// Schránka důvěry (/schranka-duvery/): replaces the old site's Contact Form 7 form. The message is e-mailed to the
// school through Resend (as news notices are); nothing is stored. The sender's name is optional (anonymity).
//
// Env: RESEND_API_KEY, TRUST_TO (recipients, default skola@zsmr.cz), MAIL_FROM (default "Schránka důvěry <schranka@zsmr.eu>")
const env = (k, d = "") => process.env[k] || d;
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
const EMAIL = /^[^\s@<>"]+@[^\s@<>"]+\.[^\s@<>"]+$/;
const recent = new Map();  // ip -> timestamps; best effort per instance

async function readBody(req) {
  if (req.body && typeof req.body === "object") return req.body;  // Vercel parses JSON and urlencoded bodies
  const chunks = [];
  for await (const c of req) chunks.push(c);
  const raw = Buffer.concat(chunks).toString("utf8");
  try { return JSON.parse(raw || "{}"); } catch { return Object.fromEntries(new URLSearchParams(raw)); }
}

function check(b) {
  const f = { name: String(b.name || "").trim(), email: String(b.email || "").trim(), subject: String(b.subject || "").trim(), message: String(b.message || "").trim() };
  if (!EMAIL.test(f.email) || f.email.length > 200) return [null, "email"];
  if (!f.message || f.message.length > 10000 || f.name.length > 120 || f.subject.length > 200) return [null, "message"];
  return [f, null];
}

module.exports = async (req, res) => {
  const send = (status, data) => { res.statusCode = status; res.setHeader("Content-Type", "application/json; charset=utf-8"); res.setHeader("Cache-Control", "no-store"); res.end(JSON.stringify(data)); };
  if (req.method !== "POST") { res.setHeader("Allow", "POST"); return send(405, { error: "method" }); }
  const origin = req.headers.origin;
  if (origin && new URL(origin).host !== req.headers.host) return send(403, { error: "origin" });
  const b = await readBody(req);
  if (b.website) return send(200, { ok: true });  // honeypot: bots fill every field; pretend success
  const [f, err] = check(b);
  if (err) return send(400, { error: err });
  const ip = String(req.headers["x-forwarded-for"] || "").split(",")[0] || "?";
  const now = Date.now(), times = (recent.get(ip) || []).filter((t) => now - t < 3600e3);
  if (times.length >= 5) return send(429, { error: "rate" });
  recent.set(ip, [...times, now]);
  if (!env("RESEND_API_KEY")) return send(503, { error: "config" });
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST", headers: { Authorization: `Bearer ${env("RESEND_API_KEY")}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      from: env("MAIL_FROM", "Schránka důvěry <schranka@zsmr.eu>"), to: env("TRUST_TO", "skola@zsmr.cz").split(/[,;\s]+/).filter(Boolean),
      reply_to: f.email, subject: `Schránka důvěry: ${f.subject || "nová zpráva"}`,
      html: `<p><b>Jméno:</b> ${esc(f.name || "neuvedeno")}<br><b>E-mail pro odpověď:</b> ${esc(f.email)}</p><p>${esc(f.message).replace(/\n/g, "<br>")}</p>`,
    }),
  }).catch(() => null);
  return r && r.ok ? send(200, { ok: true }) : send(502, { error: "mail" });
};

module.exports._check = check;
