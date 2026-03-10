import { useState } from "react";

const nodes = {
  main: {
    id: "main", label: "main.py", lang: "Python", color: "#3b82f6",
    description: "The orchestrator. Runs everything in order by calling the other modules and passing data between them via subprocess calls and JSON files.",
    position: { x: 340, y: 20 },
  },
  config: {
    id: "config", label: "config.json", lang: "Config", color: "#8b5cf6",
    description: "A simple JSON file storing your target settings: IP/domain to scan, port range, scan speed, and output preferences. Written by you, read by C#.",
    position: { x: 80, y: 160 },
  },
  recon1: {
    id: "recon1", label: "ReconProcessor\n--config mode", lang: "C#", color: "#10b981",
    description: "First C# call. Reads config.json, validates the target IP/domain and settings. If something is wrong (e.g. invalid IP), it exits early before any scanning starts.",
    position: { x: 330, y: 160 },
  },
  scanner: {
    id: "scanner", label: "scanner.py", lang: "Python", color: "#3b82f6",
    description: "Uses Python's socket library to scan ports manually, then calls nmap via subprocess for a deeper scan. Outputs open ports and service info to results.json.",
    position: { x: 100, y: 310 },
  },
  whois: {
    id: "whois", label: "whois_lookup.py", lang: "Python", color: "#3b82f6",
    description: "Uses python-whois and dnspython to grab domain registration info and DNS records (A, MX, TXT). Appends its findings to results.json.",
    position: { x: 370, y: 310 },
  },
  nmap: {
    id: "nmap", label: "nmap (CLI tool)", lang: "Tool", color: "#f59e0b",
    description: "Industry-standard network scanner. Called by scanner.py via Python's subprocess module. You don't write this — you learn to drive it from Python.",
    position: { x: 600, y: 310 },
  },
  results: {
    id: "results", label: "results.json", lang: "Data", color: "#8b5cf6",
    description: "The central data file. scanner.py and whois_lookup.py both write their findings here. C# reads this file to generate the final report.",
    position: { x: 340, y: 460 },
  },
  recon2: {
    id: "recon2", label: "ReconProcessor\n--report mode", lang: "C#", color: "#10b981",
    description: "Second C# call. Reads results.json using ConfigLoader, then hands the data to ReportGenerator which builds and writes the final report.html file.",
    position: { x: 330, y: 590 },
  },
  report: {
    id: "report", label: "report.html", lang: "Output", color: "#ef4444",
    description: "The final output. A color-coded HTML file showing open ports (red), DNS records (table), and scan metadata. Open it in any browser to view your results.",
    position: { x: 340, y: 720 },
  },
};

const edges = [
  { from: "main", to: "config", label: "reads" },
  { from: "main", to: "recon1", label: "calls" },
  { from: "config", to: "recon1", label: "validates" },
  { from: "recon1", to: "scanner", label: "triggers" },
  { from: "recon1", to: "whois", label: "triggers" },
  { from: "nmap", to: "scanner", label: "called by" },
  { from: "scanner", to: "results", label: "writes" },
  { from: "whois", to: "results", label: "writes" },
  { from: "results", to: "recon2", label: "read by" },
  { from: "recon2", to: "report", label: "generates" },
];

const langColors = {
  Python: "#3b82f6", "C#": "#10b981", Config: "#8b5cf6",
  Data: "#8b5cf6", Tool: "#f59e0b", Output: "#ef4444",
};

const weeks = [
  {
    week: 1, title: "Port Scanner", color: "#3b82f6",
    tasks: [
      { text: "Set up Codespaces repo & folder structure", file: null },
      { text: "Write scanner.py using Python's socket library", file: "scanner.py" },
      { text: "Manually scan localhost ports 20–1024", file: null },
      { text: "Install nmap and call it via subprocess", file: "scanner.py" },
      { text: "Write open port results to results.json", file: "results.json" },
    ],
    learn: "TCP connections, port states, subprocess calls",
  },
  {
    week: 2, title: "WHOIS & DNS Recon", color: "#8b5cf6",
    tasks: [
      { text: "pip install python-whois dnspython", file: null },
      { text: "Write whois_lookup.py to fetch domain info", file: "whois_lookup.py" },
      { text: "Query A, MX, and TXT DNS records", file: "whois_lookup.py" },
      { text: "Append DNS results to results.json", file: "results.json" },
      { text: "Test against a domain you own or use example.com", file: null },
    ],
    learn: "DNS record types, WHOIS data, JSON appending",
  },
  {
    week: 3, title: "C# Config + Setup", color: "#10b981",
    tasks: [
      { text: "Create ReconProcessor C# console app with dotnet new", file: null },
      { text: "Write ConfigLoader.cs to read config.json", file: "ConfigLoader.cs" },
      { text: "Add --config and --report mode switching in Program.cs", file: "Program.cs" },
      { text: "Validate IP/domain format and port range in C#", file: "ConfigLoader.cs" },
      { text: "Call ReconProcessor from main.py via subprocess", file: "main.py" },
    ],
    learn: "C# console apps, JSON parsing, inter-process calls",
  },
  {
    week: 4, title: "Report Generator & Wiring", color: "#ef4444",
    tasks: [
      { text: "Write ReportGenerator.cs to read results.json", file: "ReportGenerator.cs" },
      { text: "Build HTML string with color-coded port/DNS tables", file: "ReportGenerator.cs" },
      { text: "Write output to report.html", file: "report.html" },
      { text: "Write main.py to orchestrate all steps end-to-end", file: "main.py" },
      { text: "Run a full scan and open the report in browser!", file: null },
    ],
    learn: "HTML generation from code, full pipeline automation",
  },
];

function getCenter(node) {
  const w = 150, h = 48;
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
      {/* Header */}
      <div style={{ padding: "24px 24px 0" }}>
        <h2 style={{ textAlign: "center", marginBottom: 4, fontSize: 22, fontWeight: 700, letterSpacing: 1 }}>ReconKit</h2>
        <p style={{ textAlign: "center", color: "#94a3b8", marginBottom: 20, fontSize: 13 }}>Your cybersecurity project dashboard</p>
        <div style={{ display: "flex", justifyContent: "center", gap: 8, marginBottom: 24 }}>
          {["flow", "roadmap"].map(t => (
            <button key={t} onClick={() => setTab(t)} style={{
              padding: "8px 28px", borderRadius: 8, border: "none", cursor: "pointer",
              fontSize: 14, fontWeight: 600, transition: "all 0.15s",
              background: tab === t ? "#3b82f6" : "#1e293b",
              color: tab === t ? "#fff" : "#94a3b8",
            }}>{t === "flow" ? "📡 File Flow" : "🗺️ Roadmap"}</button>
          ))}
        </div>
      </div>

      {/* FLOW TAB */}
      {tab === "flow" && (
        <div style={{ padding: "0 24px 24px" }}>
          {/* Legend */}
          <div style={{ display: "flex", gap: 16, justifyContent: "center", marginBottom: 16, flexWrap: "wrap" }}>
            {Object.entries(langColors).map(([lang, color]) => (
              <div key={lang} style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 12 }}>
                <div style={{ width: 12, height: 12, borderRadius: 3, background: color }} />
                <span style={{ color: "#cbd5e1" }}>{lang}</span>
              </div>
            ))}
          </div>

          {/* Info box */}
          <div style={{
            minHeight: 80, background: "#1e293b",
            border: `1.5px solid ${active ? langColors[active.lang] : "#334155"}`,
            borderRadius: 10, padding: "14px 20px",
            maxWidth: 780, margin: "0 auto 20px auto", transition: "border-color 0.2s",
          }}>
            {active ? (
              <>
                <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 6 }}>
                  <span style={{ background: langColors[active.lang], color: "#fff", borderRadius: 5, padding: "2px 10px", fontSize: 11, fontWeight: 700, letterSpacing: 0.5 }}>{active.lang}</span>
                  <span style={{ fontWeight: 700, fontSize: 15 }}>{active.label.replace("\n", " ")}</span>
                </div>
                <p style={{ color: "#cbd5e1", fontSize: 13, margin: 0, lineHeight: 1.6 }}>{active.description}</p>
              </>
            ) : (
              <p style={{ color: "#475569", margin: 0, fontSize: 13, textAlign: "center", paddingTop: 22 }}>Click any node below to see what it does</p>
            )}
          </div>

          {/* SVG */}
          <div style={{ overflowX: "auto" }}>
            <svg width={780} height={800} style={{ display: "block", margin: "0 auto" }}>
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
                const w = 150, h = 48, isSelected = selected === node.id;
                const lines = node.label.split("\n");
                return (
                  <g key={node.id} transform={`translate(${node.position.x},${node.position.y})`} style={{ cursor: "pointer" }} onClick={() => setSelected(isSelected ? null : node.id)}>
                    <rect width={w} height={h} rx={8}
                      fill={isSelected ? node.color : "#1e293b"}
                      stroke={node.color} strokeWidth={isSelected ? 2.5 : 1.5}
                      style={{ transition: "all 0.15s" }}
                    />
                    {lines.map((line, li) => (
                      <text key={li} x={w / 2} y={lines.length === 1 ? h / 2 : (li === 0 ? 16 : 34)}
                        textAnchor="middle" dominantBaseline="middle"
                        fontSize={11} fontWeight={600}
                        fill={isSelected ? "#fff" : "#e2e8f0"}
                        style={{ pointerEvents: "none", userSelect: "none" }}
                      >{line}</text>
                    ))}
                  </g>
                );
              })}
            </svg>
          </div>
        </div>
      )}

      {/* ROADMAP TAB */}
      {tab === "roadmap" && (
        <div style={{ padding: "0 24px 40px", maxWidth: 800, margin: "0 auto" }}>
          {/* Overall progress */}
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

          {/* Week cards */}
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
                          display: "flex", alignItems: "center", justifyContent: "center", transition: "all 0.15s",
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