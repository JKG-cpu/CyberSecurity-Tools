import { useState } from "react";

const nodes = {
  main: {
    id: "main", label: "main.py", lang: "Python", color: "#3b82f6",
    description: "Orchestrator. Handles --hash, --crack, --strength, and --config args via argparse. Wires all Python modules together and prints results to the terminal.",
    position: { x: 300, y: 20 },
  },
  config: {
    id: "config", label: "config.json", lang: "Config", color: "#8b5cf6",
    description: "Stores settings: hash_type (sha256/sha1/md5), wordlist_path, and check_breaches toggle. Read at startup by main.py.",
    position: { x: 60, y: 160 },
  },
  hashid: {
    id: "hashid", label: "hash_identifier.py", lang: "Python", color: "#3b82f6",
    description: "Detects hash type from a given hash string using length and character patterns. Returns MD5, SHA1, SHA256, bcrypt etc. Used before cracking so you don't need to specify the type manually.",
    position: { x: 60, y: 320 },
  },
  cracker: {
    id: "cracker", label: "wordlist_cracker.py", lang: "Python", color: "#3b82f6",
    description: "Takes a hash and a wordlist file. Picks the right hash function once before the loop, then hashes each word and compares to the target. Returns the plaintext password if found.",
    position: { x: 240, y: 320 },
  },
  scorer: {
    id: "scorer", label: "strength_scorer.py", lang: "Python", color: "#3b82f6",
    description: "Scores a plaintext password 0-100. Checks length (up to 40pts), character variety (20pts), repeated characters (proportional penalty), and common passwords (-20). Returns score + grade.",
    position: { x: 420, y: 320 },
  },
  hibp: {
    id: "hibp", label: "hibp_checker.py", lang: "Python", color: "#3b82f6",
    description: "Uses HaveIBeenPwned's k-anonymity API. Sends only the first 5 chars of the SHA1 hash — never the full password. Returns how many times the password appeared in real breach data.",
    position: { x: 600, y: 320 },
  },
  history: {
    id: "history", label: "history.json", lang: "Data", color: "#8b5cf6",
    description: "Cumulative list of all past audit results. Every run appends the latest result. Lets you track audits over time.",
    position: { x: 300, y: 480 },
  },
  terminal: {
    id: "terminal", label: "terminal output", lang: "Output", color: "#ef4444",
    description: "Final output. Rich-formatted terminal display showing hash type, cracked value, strength grade, breach count, and detailed scoring breakdown via --details flag.",
    position: { x: 300, y: 620 },
  },
};

const edges = [
  { from: "main", to: "config", label: "reads" },
  { from: "main", to: "hashid", label: "calls" },
  { from: "main", to: "cracker", label: "calls" },
  { from: "main", to: "scorer", label: "calls" },
  { from: "main", to: "hibp", label: "calls" },
  { from: "hashid", to: "cracker", label: "type →" },
  { from: "cracker", to: "history", label: "appends" },
  { from: "scorer", to: "history", label: "appends" },
  { from: "hibp", to: "history", label: "appends" },
  { from: "history", to: "terminal", label: "read by" },
  { from: "main", to: "terminal", label: "prints" },
];

const langColors = {
  Python: "#3b82f6", Config: "#8b5cf6",
  Data: "#8b5cf6", Output: "#ef4444",
};

const weeks = [
  {
    week: 1, title: "Hash ID + Wordlist Cracker", color: "#3b82f6",
    tasks: [
      { text: "Set up project structure and config.json", file: null },
      { text: "Write hash_identifier.py using length + pattern detection", file: "hash_identifier.py" },
      { text: "Generate test hashes with Python's hashlib", file: null },
      { text: "Write wordlist_cracker.py to crack MD5/SHA1/SHA256", file: "wordlist_cracker.py" },
      { text: "Download a wordlist (rockyou.txt or similar)", file: null },
    ],
    learn: "How hashing works, rainbow tables, wordlist attacks",
  },
  {
    week: 2, title: "Strength Scorer + HIBP", color: "#8b5cf6",
    tasks: [
      { text: "Write strength_scorer.py with length/complexity checks", file: "strength_scorer.py" },
      { text: "Add common pattern detection (password123, qwerty, etc.)", file: "strength_scorer.py" },
      { text: "pip install requests for API calls", file: null },
      { text: "Write hibp_checker.py using k-anonymity API", file: "hibp_checker.py" },
      { text: "Understand why only 5 chars of the hash are sent", file: null },
    ],
    learn: "Password strength rules, k-anonymity, breach databases",
  },
  {
    week: 3, title: "main.py + UI + Polish", color: "#10b981",
    tasks: [
      { text: "Wire all modules together in main.py", file: "main.py" },
      { text: "Add rich terminal UI with --details flag", file: "main.py" },
      { text: "Add history.json append logic to FileLoader", file: "helpers.py" },
      { text: "Write a solid README explaining the project", file: null },
      { text: "Commit everything to GitHub!", file: null },
    ],
    learn: "CLI design, pipeline automation, project documentation",
  },
];

function getCenter(node) {
  const w = 160, h = 48;
  return { x: node.position.x + w / 2, y: node.position.y + h / 2 };
}

export default function App() {
  const [tab, setTab] = useState("flow");
  const [selected, setSelected] = useState(null);
  const [checked, setChecked] = useState({});
  const active = selected ? nodes[selected] : null;

  const toggleCheck = (key) => setChecked(p => ({ ...p, [key]: !p[key] }));
  const totalTasks = weeks.reduce((a, w) => a + w.tasks.length, 0);
  const doneTasks = Object.values(checked).filter(Boolean).length;
  const progress = Math.round((doneTasks / totalTasks) * 100);

  return (
    <div style={{ fontFamily: "sans-serif", background: "#0f172a", minHeight: "100vh", color: "#f1f5f9" }}>
      <div style={{ padding: "24px 24px 0" }}>
        <h2 style={{ textAlign: "center", marginBottom: 4, fontSize: 22, fontWeight: 700, letterSpacing: 1 }}>CredAudit</h2>
        <p style={{ textAlign: "center", color: "#94a3b8", marginBottom: 20, fontSize: 13 }}>Password Auditor & Credential Analyzer</p>
        <div style={{ display: "flex", justifyContent: "center", gap: 8, marginBottom: 24 }}>
          {["flow", "roadmap"].map(t => (
            <button key={t} onClick={() => setTab(t)} style={{
              padding: "8px 28px", borderRadius: 8, border: "none", cursor: "pointer",
              fontSize: 14, fontWeight: 600, transition: "all 0.15s",
              background: tab === t ? "#3b82f6" : "#1e293b",
              color: tab === t ? "#fff" : "#94a3b8",
            }}>{t === "flow" ? "🔐 File Flow" : "🗺️ Roadmap"}</button>
          ))}
        </div>
      </div>

      {tab === "flow" && (
        <div style={{ padding: "0 24px 24px" }}>
          <div style={{ display: "flex", gap: 16, justifyContent: "center", marginBottom: 16, flexWrap: "wrap" }}>
            {Object.entries(langColors).map(([lang, color]) => (
              <div key={lang} style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 12 }}>
                <div style={{ width: 12, height: 12, borderRadius: 3, background: color }} />
                <span style={{ color: "#cbd5e1" }}>{lang}</span>
              </div>
            ))}
          </div>
          <div style={{
            minHeight: 80, background: "#1e293b",
            border: `1.5px solid ${active ? langColors[active.lang] : "#334155"}`,
            borderRadius: 10, padding: "14px 20px",
            maxWidth: 780, margin: "0 auto 20px auto",
          }}>
            {active ? (
              <>
                <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 6 }}>
                  <span style={{ background: langColors[active.lang], color: "#fff", borderRadius: 5, padding: "2px 10px", fontSize: 11, fontWeight: 700 }}>{active.lang}</span>
                  <span style={{ fontWeight: 700, fontSize: 15 }}>{active.label}</span>
                </div>
                <p style={{ color: "#cbd5e1", fontSize: 13, margin: 0, lineHeight: 1.6 }}>{active.description}</p>
              </>
            ) : (
              <p style={{ color: "#475569", margin: 0, fontSize: 13, textAlign: "center", paddingTop: 22 }}>Click any node below to see what it does</p>
            )}
          </div>
          <div style={{ overflowX: "auto" }}>
            <svg width={780} height={700} style={{ display: "block", margin: "0 auto" }}>
              <defs>
                <marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
                  <path d="M0,0 L0,6 L8,3 z" fill="#475569" />
                </marker>
              </defs>
              {edges.map((e, i) => {
                const f = getCenter(nodes[e.from]), t = getCenter(nodes[e.to]);
                const mx = (f.x + t.x) / 2, my = (f.y + t.y) / 2;
                const dx = t.x - f.x, dy = t.y - f.y;
                const len = Math.sqrt(dx * dx + dy * dy) || 1;
                const nx = (-dy / len) * 18, ny = (dx / len) * 18;
                return (
                  <g key={i}>
                    <line x1={f.x} y1={f.y} x2={t.x} y2={t.y} stroke="#334155" strokeWidth={1.5} markerEnd="url(#arrow)" />
                    <text x={mx + nx} y={my + ny} fontSize={10} fill="#64748b" textAnchor="middle" dominantBaseline="middle" style={{ userSelect: "none" }}>{e.label}</text>
                  </g>
                );
              })}
              {Object.values(nodes).map((node) => {
                const w = 160, h = 48, isSelected = selected === node.id;
                return (
                  <g key={node.id} transform={`translate(${node.position.x},${node.position.y})`} style={{ cursor: "pointer" }} onClick={() => setSelected(isSelected ? null : node.id)}>
                    <rect width={w} height={h} rx={8}
                      fill={isSelected ? node.color : "#1e293b"}
                      stroke={node.color} strokeWidth={isSelected ? 2.5 : 1.5}
                    />
                    <text x={w / 2} y={h / 2} textAnchor="middle" dominantBaseline="middle"
                      fontSize={11} fontWeight={600}
                      fill={isSelected ? "#fff" : "#e2e8f0"}
                      style={{ pointerEvents: "none", userSelect: "none" }}
                    >{node.label}</text>
                  </g>
                );
              })}
            </svg>
          </div>
        </div>
      )}

      {tab === "roadmap" && (
        <div style={{ padding: "0 24px 40px", maxWidth: 800, margin: "0 auto" }}>
          <div style={{ background: "#1e293b", borderRadius: 10, padding: "16px 20px", marginBottom: 28 }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
              <span style={{ fontSize: 13, color: "#94a3b8" }}>Overall Progress</span>
              <span style={{ fontSize: 13, fontWeight: 700 }}>{doneTasks}/{totalTasks} tasks</span>
            </div>
            <div style={{ background: "#0f172a", borderRadius: 999, height: 10, overflow: "hidden" }}>
              <div style={{ width: `${progress}%`, height: "100%", background: "linear-gradient(90deg, #3b82f6, #10b981)", borderRadius: 999, transition: "width 0.3s" }} />
            </div>
            <div style={{ textAlign: "right", fontSize: 12, color: "#64748b", marginTop: 4 }}>{progress}% complete</div>
          </div>
          {weeks.map((w) => {
            const weekDone = w.tasks.filter((_, i) => checked[`${w.week}-${i}`]).length;
            return (
              <div key={w.week} style={{ background: "#1e293b", borderRadius: 12, marginBottom: 20, overflow: "hidden" }}>
                <div style={{ background: w.color + "22", borderLeft: `4px solid ${w.color}`, padding: "14px 20px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <div>
                    <span style={{ fontSize: 11, fontWeight: 700, color: w.color, letterSpacing: 1, textTransform: "uppercase" }}>Week {w.week}</span>
                    <h3 style={{ margin: "2px 0 0", fontSize: 16, fontWeight: 700 }}>{w.title}</h3>
                  </div>
                  <div style={{ textAlign: "right" }}>
                    <div style={{ fontSize: 12, color: "#64748b" }}>{weekDone}/{w.tasks.length}</div>
                    <div style={{ background: "#0f172a", borderRadius: 999, height: 6, width: 80, marginTop: 4, overflow: "hidden" }}>
                      <div style={{ width: `${(weekDone / w.tasks.length) * 100}%`, height: "100%", background: w.color, borderRadius: 999, transition: "width 0.3s" }} />
                    </div>
                  </div>
                </div>
                <div style={{ padding: "12px 20px" }}>
                  {w.tasks.map((task, i) => {
                    const key = `${w.week}-${i}`;
                    const done = checked[key];
                    return (
                      <div key={i} onClick={() => toggleCheck(key)}
                        style={{ display: "flex", alignItems: "center", gap: 12, padding: "8px 4px", cursor: "pointer", borderRadius: 6 }}
                        onMouseEnter={e => e.currentTarget.style.background = "#0f172a"}
                        onMouseLeave={e => e.currentTarget.style.background = "transparent"}
                      >
                        <div style={{
                          width: 18, height: 18, borderRadius: 4, flexShrink: 0,
                          border: `2px solid ${done ? w.color : "#475569"}`,
                          background: done ? w.color : "transparent",
                          display: "flex", alignItems: "center", justifyContent: "center",
                        }}>
                          {done && <span style={{ color: "#fff", fontSize: 11, fontWeight: 700 }}>✓</span>}
                        </div>
                        <span style={{ fontSize: 13, flex: 1, color: done ? "#475569" : "#cbd5e1", textDecoration: done ? "line-through" : "none" }}>{task.text}</span>
                        {task.file && (
                          <span style={{ fontSize: 11, color: "#64748b", background: "#0f172a", padding: "2px 8px", borderRadius: 4, fontFamily: "monospace", flexShrink: 0 }}>{task.file}</span>
                        )}
                      </div>
                    );
                  })}
                </div>
                <div style={{ padding: "4px 20px 14px" }}>
                  <span style={{ fontSize: 11, color: "#64748b" }}>📚 You'll learn: </span>
                  <span style={{ fontSize: 11, color: "#94a3b8" }}>{w.learn}</span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}