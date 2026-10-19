// node tests/trust.test.js — Schránka důvěry endpoint, Resend stubbed
const assert = require("assert");
const handler = require("../api/trust.js");
let sent = null;
global.fetch = async (url, opts) => { sent = JSON.parse(opts.body); return { ok: true }; };
process.env.RESEND_API_KEY = "k";
const call = (body, headers = {}) => new Promise((done) => {
  const res = { headers: {}, setHeader(k, v) { this.headers[k] = v; }, end(d) { done({ status: this.statusCode, body: JSON.parse(d) }); } };
  handler({ method: "POST", headers: { host: "www.zsmr.eu", origin: "https://www.zsmr.eu", "x-forwarded-for": headers.ip || "1.1.1.1", ...headers }, body }, res);
});
(async () => {
  assert.equal((await call({ email: "x", message: "a" })).status, 400);
  assert.equal((await call({ email: "a@b.cz", message: "" })).status, 400);
  assert.equal((await call({ email: "a@b.cz", message: "hi", website: "spam" })).body.ok, true);
  assert.equal(sent, null, "honeypot must not send");
  const ok = await call({ email: "a@b.cz", message: "<script>x</script>", name: "" });
  assert.equal(ok.status, 200);
  assert.ok(sent.html.includes("&lt;script&gt;") && sent.html.includes("neuvedeno") && sent.reply_to === "a@b.cz");
  assert.equal((await call({ email: "a@b.cz", message: "x" }, { origin: "https://evil.example" })).status, 403);
  for (let i = 0; i < 4; i++) await call({ email: "a@b.cz", message: "x" }, { ip: "9.9.9.9" });
  assert.equal((await call({ email: "a@b.cz", message: "x" }, { ip: "9.9.9.9" })).status, 200);
  assert.equal((await call({ email: "a@b.cz", message: "x" }, { ip: "9.9.9.9" })).status, 429);
  console.log("trust tests ok");
})();
