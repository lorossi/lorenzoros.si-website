// The /shell page: the website as a fake terminal.
// The file system is built from the JSON the build embeds in the page
// (#shell-data); everything else is made up on the spot.

(() => {
  "use strict";

  const DATA = JSON.parse(document.getElementById("shell-data").textContent);
  const $ = (id) => document.getElementById(id);

  // ---------- the file system ----------

  const ABOUT = [
    "Hi, I'm Lorenzo.",
    "",
    "I'm a software engineer at CERN, building the tools used to operate its power converters.",
    "",
    "Off the clock I work on side projects: interactive experiments, small libraries,",
    "Godot games, Telegram bots, photography.",
    "",
    "Start with the interactive projects, they're the fun part:  cd interactive",
  ].join("\n");

  const mkFile = (content, date, extra = {}) => ({ type: "file", content, date, ...extra });
  const mkDir = (children) => {
    let date = "";
    for (const child of Object.values(children)) if (child.date > date) date = child.date;
    if (!date) date = DATA.built;
    return { type: "dir", children, date };
  };

  const repoFile = (r, launch) => {
    const lines = [`# ${r.name}`, "", r.description || "(no description)", ""];
    if (launch) lines.push(`updated ${r.date}`, `→ ${r.url}`, "", `run  open ${r.name}.url  to launch it`);
    else lines.push(`last push ${r.date}`, `→ ${r.url}`);
    return mkFile(lines.join("\n"), r.date, { url: r.url });
  };

  const buildFs = () => {
    const interactive = {};
    for (const r of DATA.interactive) interactive[`${r.name}.url`] = repoFile(r, true);

    const portfolio = {};
    for (const [lang, repos] of Object.entries(DATA.portfolio)) {
      const files = {};
      for (const r of repos) files[`${r.name}.md`] = repoFile(r, false);
      portfolio[lang] = mkDir(files);
    }

    const blog = {};
    for (const a of DATA.articles) blog[`${a.slug}.md`] = mkFile(a.source, a.date, { url: a.url });

    const contacts = {};
    for (const c of DATA.contacts) {
      contacts[c.name] = c.href
        ? mkFile(`${c.text} ${c.label}\n→ ${c.href}`, DATA.built, { url: c.href })
        : mkFile("", DATA.built, { locked: true, what: c.label });
    }

    return mkDir({
      "about.txt": mkFile(ABOUT, DATA.built),
      blog: mkDir(blog),
      contacts: mkDir(contacts),
      interactive: mkDir(interactive),
      portfolio: mkDir(portfolio),
    });
  };

  const ROOT = buildFs();
  const sorted = (dir) => Object.keys(dir.children).sort();
  const dispPath = (p) => `~${p.length ? `/${p.join("/")}` : ""}`;

  const resolve = (cwd, raw) => {
    let p = raw || "";
    let base;
    if (!p) base = cwd.slice();
    else if (p === "~") base = [];
    else if (p.startsWith("~")) {
      base = [];
      p = p.slice(1);
    } else if (p.startsWith("/home/lorenzo")) {
      base = [];
      p = p.slice(13);
    } else if (p.startsWith("/")) base = [];
    else base = cwd.slice();
    if (p && p !== "~") {
      for (const s of p.split("/")) {
        if (!s || s === ".") continue;
        if (s === "..") base.pop();
        else base.push(s);
      }
    }
    let node = ROOT;
    for (const s of base) {
      if (node.type !== "dir" || !node.children[s]) return { err: true, path: base };
      node = node.children[s];
    }
    return { path: base, node };
  };

  const allFiles = (node, path, out) => {
    for (const k of sorted(node)) {
      const child = node.children[k];
      const p = path.concat([k]);
      if (child.type === "dir") {
        allFiles(child, p, out);
        out.push({ dir: true, p: dispPath(p) });
      } else out.push({ dir: false, p: dispPath(p) });
    }
    return out;
  };

  // ---------- output lines: { segs: [{ t, role, bold, cmd, href }] } ----------

  const T = (t, role = "fg", bold = false) => ({ t, role, bold });
  const C = (t, cmd, role = "fg", bold = false) => ({ t, cmd, role, bold });
  const Lk = (t, href) => ({ t, href, role: "acc" });
  const line = (...segs) => ({ segs });
  const txt = (s, role) => line(T(s, role));

  const linkify = (s, role, bold) =>
    s
      .split(/(https?:\/\/[^\s)]+)/)
      .map((p, i) => (p ? (i % 2 ? Lk(p, p) : T(p, role, bold)) : null))
      .filter(Boolean);

  const fileLines = (name, content) => {
    const md = name.endsWith(".md");
    let front = false;
    let fence = false;
    return content.split("\n").map((l) => {
      let role = "fg";
      let bold = false;
      if (md) {
        if (l === "+++") {
          front = !front;
          role = "dim";
        } else if (front) role = "dim";
        else if (l.startsWith("```")) {
          fence = !fence;
          role = "dim";
        } else if (fence) role = "dim";
        else if (/^#{1,6} /.test(l)) {
          role = "acc";
          bold = true;
        } else if (l.startsWith("> ")) role = "dim";
      }
      return { segs: linkify(l, role, bold), role, bold, text: l };
    });
  };

  const pad = (s, n) => String(s).padEnd(n);
  const lpad = (s, n) => String(s).padStart(n);
  const rep = (c, n) => (n > 0 ? c.repeat(n) : "");

  // ---------- toys ----------

  // enigma: rotors I II III, reflector B, start AAA, no plugboard
  const ROT = ["EKMFLGDQVZNTOWYHXUSPAIBRCJ", "AJDKSIRUXBLHWTMCQGZNPYFVOE", "BDFHJLCPRTXVZNYEIWGAKMUSQO"];
  const REFL = "YRUHQSLDPXNGOKMIEBFZCWVJAT";
  const INV = ROT.map((w) => {
    const a = [];
    for (let i = 0; i < 26; i++) a[w.charCodeAt(i) - 65] = i;
    return a;
  });
  const enigma = (text) => {
    const pos = [0, 0, 0];
    return text.toUpperCase().replace(/[A-Z]/g, (ch) => {
      const middle = pos[1] === 4;
      const right = pos[2] === 21;
      if (middle) {
        pos[0] = (pos[0] + 1) % 26;
        pos[1] = (pos[1] + 1) % 26;
      } else if (right) pos[1] = (pos[1] + 1) % 26;
      pos[2] = (pos[2] + 1) % 26;
      let c = ch.charCodeAt(0) - 65;
      for (let i = 2; i >= 0; i--) c = (ROT[i].charCodeAt((c + pos[i]) % 26) - 65 - pos[i] + 26) % 26;
      c = REFL.charCodeAt(c) - 65;
      for (let j = 0; j < 3; j++) c = (INV[j][(c + pos[j]) % 26] - pos[j] + 26) % 26;
      return String.fromCharCode(c + 65);
    });
  };

  const decimalTime = (d) => {
    const s = d.getHours() * 3600 + d.getMinutes() * 60 + d.getSeconds() + d.getMilliseconds() / 1000;
    const dec = Math.floor((s / 86400) * 100000);
    const two = (n) => String(n).padStart(2, "0");
    return `${Math.floor(dec / 10000)}:${two(Math.floor(dec / 100) % 100)}:${two(dec % 100)}`;
  };

  const CORGI = [
    "      /\\    /\\",
    "     /  \\__/  \\",
    "    (  o    o  )___________________",
    "     \\    v   /                    \\",
    "      '-.__.-'                      )~",
    "        \\__________________________/",
    "          ||  ||             ||  ||",
    "          ''  ''             ''  ''",
  ];

  const LOGO = [
    "██╗      ██████╗ ",
    "██║      ██╔══██╗",
    "██║      ██████╔╝",
    "██║      ██╔══██╗",
    "███████╗ ██║  ██║",
    "╚══════╝ ╚═╝  ╚═╝",
  ];

  const SMOKE = [
    "              (@@)   (  )    (@)   ( )     (@@)",
    "              (  )  (@@)   ( )    (@)   ( )",
  ];
  const TRAIN = [
    "         ( )",
    "        _||_____________   _____________________   _____________________   _____________________",
    "       |  ||   _____    |  |                     | |                     | |                     |",
    "      /|  ||  | o o |   |==|    ./interactive    |=|     ./portfolio     |=|       ./blog        |",
    "     /_|__||__|_____|___|  |_____________________| |_____________________| |_____________________|",
    "        (O)(O)    (O)(O)      (O)(O)       (O)(O)   (O)(O)       (O)(O)   (O)(O)       (O)(O)",
  ];
  const TRAIN_W = Math.max(...TRAIN.map((l) => l.length));

  const KONAMI = "ArrowUp,ArrowUp,ArrowDown,ArrowDown,ArrowLeft,ArrowRight,ArrowLeft,ArrowRight,b,a";
  const ACCENTS = ["cyan", "green", "amber", "magenta"];
  const MATRIX_CHARS = "0123456789ABCDEFlorenzosi<>*+=:/";
  const HOG = "vscode-spotify-now-playing";
  const PROCS = [
    ...new Set([
      HOG,
      ...DATA.interactive.map((r) => r.name),
      ...Object.values(DATA.portfolio)
        .flat()
        .map((r) => r.name),
    ]),
  ].slice(0, 40);

  const COMMANDS = [
    "help",
    "ls",
    "cd",
    "pwd",
    "cat",
    "less",
    "head",
    "vi",
    "vim",
    "nano",
    "open",
    "tree",
    "clear",
    "whoami",
    "history",
    "echo",
    "date",
    "exit",
    "sudo",
    "neofetch",
    "top",
    "htop",
    "matrix",
    "enigma",
    "corgi",
    "decimalclock",
    "ssh",
    "sl",
    "rm",
  ];

  // ---------- state ----------

  const t0 = Date.now();
  const st = {
    cwd: [],
    hist: [],
    hIdx: null,
    count: 0,
    editor: null, // { kind: "vi" | "nano", path, lines, msg }
    app: null, // { kind, title, quit }
    accent: null,
    kseq: [],
    timer: null,
    stream: null,
  };
  let cwd = []; // working copy while a command line runs
  let pendingEditor = null;
  let pendingApp = null;

  // ---------- rendering ----------

  const out = $("out");
  const sh = $("sh");
  const input = $("sh-input");

  const el = (tag, cls, text) => {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined) e.textContent = text;
    return e;
  };

  const segEl = (s) => {
    const cls = `c-${s.role}${s.bold ? " b" : ""}`;
    if (s.cmd) {
      const b = el("button", `cmd ${cls}`, s.t);
      b.type = "button";
      b.dataset.cmd = s.cmd;
      return b;
    }
    if (s.href) {
      const a = el("a", `lnk ${cls}`, s.t);
      a.href = s.href;
      if (!s.href.startsWith("/")) {
        a.target = "_blank";
        a.rel = "noopener";
      }
      return a;
    }
    return el("span", cls, s.t);
  };

  const lineEl = (l) => {
    const d = el("div", "tl");
    for (const s of l.segs) d.appendChild(segEl(s));
    return d;
  };

  const promptSegs = (path) => [T("lorenzo", "acc", true), T("@rossi:"), T(path, "acc"), T("$ ", "dim")];

  const fillPrompt = (node, path) => {
    node.replaceChildren(...promptSegs(path).map(segEl));
  };

  const newEntry = (path, cmd) => {
    const entry = el("div", "entry");
    if (path !== null) entry.appendChild(lineEl({ segs: promptSegs(path).concat([T(cmd)]) }));
    out.appendChild(entry);
    while (out.childElementCount > 150) out.firstElementChild.remove();
    return entry;
  };

  const printTo = (entry, lines) => {
    const frag = document.createDocumentFragment();
    for (const l of lines) frag.appendChild(lineEl(l));
    entry.appendChild(frag);
  };

  const scrollDown = () => {
    sh.scrollTop = sh.scrollHeight;
  };

  const focus = (node) => {
    try {
      node.focus({ preventScroll: true });
    } catch {
      node.focus();
    }
  };

  const refreshChrome = () => {
    const ed = st.editor;
    const app = st.app;
    $("sh").hidden = Boolean(ed || app);
    $("vi").hidden = !(ed && ed.kind === "vi") || Boolean(app);
    $("nano").hidden = !(ed && ed.kind === "nano") || Boolean(app);
    $("app").hidden = !app;
    $("term-title").textContent = app
      ? app.title
      : ed
        ? `${ed.kind} ${ed.path}`
        : `lorenzo@rossi: ${dispPath(st.cwd)}`;
    $("term-info").textContent = ed || app ? "" : `zsh — ${st.count} command${st.count === 1 ? "" : "s"}`;
    const quit = $("term-quit");
    quit.hidden = !(ed || app);
    quit.textContent = app ? app.quit : ed && ed.kind === "nano" ? "^X exit" : ":q quit";
    fillPrompt($("ps"), dispPath(st.cwd));
  };

  // ---------- editors ----------

  const openEditor = (ed) => {
    st.editor = ed;
    const rows = ed.lines.map((l, i) => ({ num: String(i + 1), l }));
    if (ed.kind === "vi") {
      const box = $("vi-rows");
      box.replaceChildren();
      for (const r of rows) {
        const row = el("div", "vi-row");
        row.append(el("span", "vi-num", r.num), el("span", `c-${r.l.role}${r.l.bold ? " b" : ""}`, r.l.text));
        box.appendChild(row);
      }
      for (let i = rows.length; i < 26; i++) {
        const row = el("div", "vi-row");
        row.append(el("span", "vi-num", ""), el("span", "c-dim", "~"));
        box.appendChild(row);
      }
      box.scrollTop = 0;
      $("vi-path").textContent = `${ed.path} [RO]`;
      $("vi-info").textContent = `${ed.lines.length}L   All`;
    } else {
      const box = $("nano-rows");
      box.replaceChildren();
      for (const r of rows) box.appendChild(el("div", `tl c-${r.l.role}${r.l.bold ? " b" : ""}`, r.l.text));
      box.scrollTop = 0;
      $("nano-path").textContent = ed.path;
    }
    edMsg(ed.msg);
    refreshChrome();
    focus(ed.kind === "vi" ? $("vi-cmd") : $("nano-key"));
  };

  const edMsg = (msg) => {
    if (!st.editor) return;
    st.editor.msg = msg;
    $("vi-cmd").placeholder = msg;
    $("nano-msg").textContent = msg;
  };

  const closeEditor = () => {
    st.editor = null;
    $("vi-cmd").value = "";
    refreshChrome();
    scrollDown();
    focus(input);
  };

  // ---------- full-screen programs ----------

  const screenSize = () => {
    const fs = Number.parseFloat(getComputedStyle(sh).fontSize) || 15;
    const box = sh.getBoundingClientRect();
    return {
      cols: Math.max(24, Math.floor((box.width - 40) / (fs * 0.6))),
      rows: Math.max(8, Math.floor((box.height - 32) / (fs * 1.6))),
    };
  };

  const drawApp = (lines) => {
    $("app-rows").replaceChildren(...lines.map(lineEl));
  };

  const startApp = (app, size, frame, every) => {
    stopTimer();
    st.app = app;
    refreshChrome();
    focus($("app-key"));
    frame(size);
    st.timer = setInterval(() => frame(size), every);
  };

  const stopTimer = () => {
    if (st.timer) clearInterval(st.timer);
    st.timer = null;
  };

  const stopApp = () => {
    stopTimer();
    st.app = null;
    refreshChrome();
    scrollDown();
    focus(input);
  };

  const startMatrix = (size) => {
    const { cols, rows } = size;
    const trail = Math.max(6, Math.floor(rows * 0.6));
    const pick = () => MATRIX_CHARS[Math.floor(Math.random() * MATRIX_CHARS.length)];
    const heads = Array.from({ length: cols }, () => -Math.floor(Math.random() * rows * 2));
    const grid = Array.from({ length: rows }, () => Array.from({ length: cols }, pick));
    const frame = () => {
      for (let c = 0; c < cols; c += 2) {
        heads[c] += 1;
        if (heads[c] - trail > rows) heads[c] = -Math.floor(Math.random() * rows);
        if (Math.random() < 0.1) grid[Math.floor(Math.random() * rows)][c] = pick();
      }
      const lines = [];
      for (let r = 0; r < rows; r++) {
        const segs = [];
        let cur = null;
        let buf = "";
        for (let c = 0; c < cols; c++) {
          const d = heads[c] - r;
          let ch = " ";
          let role = "acc";
          if (c % 2 === 0 && d >= 0 && d < trail) {
            ch = grid[r][c];
            role = d === 0 ? "fg" : d > trail * 0.6 ? "dim" : "acc";
          }
          if (role !== cur) {
            if (buf) segs.push(T(buf, cur, cur === "fg"));
            buf = "";
            cur = role;
          }
          buf += ch;
        }
        if (buf) segs.push(T(buf, cur, cur === "fg"));
        lines.push({ segs });
      }
      drawApp(lines);
    };
    startApp({ kind: "matrix", title: "matrix", quit: "any key: wake up" }, size, frame, 70);
  };

  const startTop = (size, fancy) => {
    const procs = PROCS.map((name, i) => ({
      name,
      pid: 1000 + i * 37,
      mem: Math.random() * 2 + 0.1,
      time: Math.random() * 300,
    }));
    const frame = () => {
      for (const p of procs) {
        p.cpu = p.name === HOG ? 99 + Math.random() : Math.random() < 0.3 ? Math.random() * 4 : 0;
        p.time += p.cpu / 100;
      }
      const list = procs.slice().sort((a, b) => b.cpu - a.cpu);
      const total = list.reduce((s, p) => s + p.cpu, 0);
      const up = Math.floor((Date.now() - t0) / 1000);
      const upS = `${Math.floor(up / 3600)}:${String(Math.floor(up / 60) % 60).padStart(2, "0")}:${String(up % 60).padStart(2, "0")}`;
      const load = [1 + Math.random() * 0.2, 1.05, 0.98].map((x) => x.toFixed(2));
      const fmt = (t) => `${Math.floor(t / 60)}:${(t % 60).toFixed(2).padStart(5, "0")}`;
      const lines = [];
      if (fancy) {
        const bar = (label, pct, right) => {
          const n = Math.round((pct / 100) * 30);
          return line(
            T(`${lpad(label, 3)}[`, "dim"),
            T(rep("|", n), "acc"),
            T(rep(" ", 30 - n) + lpad(`${pct.toFixed(1)}%`, 6)),
            T("]", "dim"),
            T(`   ${right}`),
          );
        };
        lines.push(bar("1", 100, `Tasks: ${procs.length} repos, 1 running`));
        lines.push(bar("2", Math.min(100, total - 97), `Load average: ${load.join(" ")}`));
        lines.push(bar("Mem", 22 + Math.random() * 2, `Uptime: ${upS}`));
      } else {
        const now = new Date().toTimeString().slice(0, 8);
        lines.push(txt(`top - ${now} up ${upS},  1 user,  load average: ${load.join(", ")}`));
        lines.push(txt(`Tasks: ${procs.length} total,   1 running, ${procs.length - 1} sleeping,   0 stopped,   0 zombie`));
        lines.push(txt(`%Cpu(s): ${(total / 4).toFixed(1)} us,  0.3 sy,  0.0 ni, ${(100 - total / 4).toFixed(1)} id`));
      }
      lines.push(txt(""), line(T("  PID USER      %CPU %MEM     TIME+ COMMAND", "acc", true)));
      for (const p of list.slice(0, Math.max(5, size.rows - 8))) {
        const hot = p.cpu > 50;
        lines.push(
          line(
            T(`${lpad(p.pid, 5)} lorenzo  ${lpad(p.cpu.toFixed(1), 5)} ${lpad(p.mem.toFixed(1), 4)} ${lpad(fmt(p.time), 9)} `, hot ? "fg" : "dim", hot),
            T(p.name, hot ? "acc" : "fg", hot),
          ),
        );
      }
      lines.push(txt(""), txt("q quit", "dim"));
      drawApp(lines);
    };
    const title = fancy ? "htop" : "top";
    startApp({ kind: "top", title, quit: "q quit" }, size, frame, 1200);
  };

  const startSl = (size) => {
    let x = size.cols;
    let f = 0;
    const top = Math.max(0, Math.floor((size.rows - TRAIN.length - 1) / 2));
    const crop = (l) => (x >= 0 ? rep(" ", x) + l : l.slice(-x)).slice(0, size.cols);
    const frame = () => {
      const lines = [];
      for (let i = 0; i < top; i++) lines.push(txt(""));
      lines.push(txt(crop(SMOKE[f % 6 < 3 ? 0 : 1]), "dim"));
      TRAIN.forEach((l, i) => lines.push(txt(crop(l), i === TRAIN.length - 1 ? "dim" : "fg")));
      drawApp(lines);
      x -= 2;
      f++;
      if (x < -TRAIN_W) stopApp();
    };
    startApp({ kind: "sl", title: "sl", quit: "you meant ls" }, size, frame, 40);
  };

  // ---------- commands ----------

  const rel = (path) => {
    const same = path.length === cwd.length + 1 && cwd.every((s, i) => s === path[i]);
    return same ? path[path.length - 1] : dispPath(path);
  };

  const cmdLs = (args) => {
    const flags = args.filter((a) => a.startsWith("-")).join("");
    const targets = args.filter((a) => !a.startsWith("-"));
    const r = resolve(cwd, targets[0]);
    if (r.err) return { ok: false, lines: [txt(`ls: cannot access '${targets[0]}': No such file or directory`)] };
    const isDir = r.node.type === "dir";
    const names = isDir ? sorted(r.node) : [r.path[r.path.length - 1]];
    const nodeOf = (n) => (isDir ? r.node.children[n] : r.node);
    const entry = (n) => {
      const nd = nodeOf(n);
      const rp = rel(isDir ? r.path.concat([n]) : r.path);
      if (nd.type === "dir") return C(`${n}/`, `cd ${rp} && ls`, "acc", true);
      return C(n, `cat ${rp}`, nd.locked ? "dim" : "fg");
    };
    if (!flags.includes("l")) {
      const segs = [];
      if (flags.includes("a")) segs.push(T(".", "acc", true), T("  "), C("..", "cd .. && ls", "acc", true), T("  "));
      names.forEach((n, i) => {
        if (i) segs.push(T("  "));
        segs.push(entry(n));
      });
      return { ok: true, lines: segs.length ? [{ segs }] : [] };
    }
    const lines = [txt(`total ${names.length}`, "dim")];
    for (const n of names) {
      const nd = nodeOf(n);
      const perm = nd.type === "dir" ? "drwxr-xr-x" : nd.locked ? "-r--------" : "-rw-r--r--";
      const owner = nd.locked ? "root   " : "lorenzo";
      const size = nd.type === "dir" ? 4096 : nd.locked ? 64 : new Blob([nd.content]).size;
      lines.push(line(T(`${perm}  ${owner} ${lpad(size, 6)}  ${nd.date}  `, "dim"), entry(n)));
    }
    return { ok: true, lines };
  };

  const cmdCat = (name, args) => {
    if (!args.length) return { ok: false, lines: [txt(`${name}: missing operand`), txt("try: cat about.txt", "dim")] };
    const lines = [];
    let ok = true;
    for (const a of args) {
      const r = resolve(cwd, a);
      if (r.err) {
        ok = false;
        lines.push(txt(`${name}: ${a}: No such file or directory`));
      } else if (r.node.type === "dir") {
        ok = false;
        lines.push(line(T(`${name}: ${a}: Is a directory  `), C(`ls ${a}`, `ls ${a}`, "acc")));
      } else if (r.node.locked) {
        ok = false;
        lines.push(
          txt(`${name}: ${a}: Permission denied`),
          txt(`  the ${r.node.what} is kept away from spambots: the homepage reveals it with JavaScript.`, "dim"),
          line(T("  see it at ", "dim"), Lk("lorenzoros.si/#contacts", "/#contacts")),
        );
      } else {
        let fl = fileLines(r.path[r.path.length - 1], r.node.content);
        if (name === "head") fl = fl.slice(0, 10);
        for (const l of fl) lines.push({ segs: l.segs });
      }
    }
    return { ok, lines };
  };

  const cmdTree = (args) => {
    const r = resolve(cwd, args[0]);
    if (r.err || r.node.type !== "dir") return { ok: false, lines: [txt(`${args[0] || "."} [error opening dir]`)] };
    const lines = [line(T(args[0] || ".", "acc", true))];
    let dirs = 0;
    let files = 0;
    const walk = (node, path, prefix) => {
      const keys = sorted(node);
      keys.forEach((k, i) => {
        const last = i === keys.length - 1;
        const child = node.children[k];
        const p = path.concat([k]);
        const branch = T(prefix + (last ? "└── " : "├── "), "dim");
        if (child.type === "dir") {
          dirs++;
          lines.push(line(branch, C(k, `cd ${dispPath(p)} && ls`, "acc", true)));
          walk(child, p, prefix + (last ? "    " : "│   "));
        } else {
          files++;
          lines.push(line(branch, C(k, `cat ${dispPath(p)}`, child.locked ? "dim" : "fg")));
        }
      });
    };
    walk(r.node, r.path, "");
    lines.push(txt(""), txt(`${dirs} directories, ${files} files`, "dim"));
    return { ok: true, lines };
  };

  const cmdEdit = (kind, name, args) => {
    if (!args.length) return { ok: false, lines: [txt(`${name}: which file? try: ${name} about.txt`, "dim")] };
    const r = resolve(cwd, args[0]);
    if (r.err) return { ok: false, lines: [txt(`${name}: ${args[0]}: No such file (and this file system is read-only, so no new ones)`)] };
    if (r.node.type === "dir") return { ok: false, lines: [txt(`"${args[0]}" is a directory`)] };
    if (r.node.locked) return { ok: false, lines: [txt(`"${args[0]}" [Permission Denied]`)] };
    const lines = fileLines(r.path[r.path.length - 1], r.node.content);
    const bytes = new Blob([r.node.content]).size;
    const msg =
      kind === "vi"
        ? `"${args[0]}" [readonly] ${lines.length}L, ${bytes}B   —   :q to quit`
        : `[ Read ${lines.length} lines (read-only) ]`;
    pendingEditor = { kind, path: dispPath(r.path), lines, msg };
    return { ok: true, lines: [] };
  };

  const cmdOpen = (args) => {
    if (!args.length) return { ok: false, lines: [txt("open: which one? try: ls ~/interactive", "dim")] };
    const r = resolve(cwd, args[0]);
    if (r.err) return { ok: false, lines: [txt(`open: ${args[0]}: No such file or directory`)] };
    if (!r.node.url) return { ok: false, lines: [txt(`open: nothing to launch in ${args[0]}, try cat ${args[0]}`, "dim")] };
    if (r.node.url.startsWith("/")) window.location.href = r.node.url;
    else window.open(r.node.url, "_blank", "noopener");
    return { ok: true, lines: [line(T("opening ", "dim"), Lk(r.node.url, r.node.url))] };
  };

  const cmdNeofetch = () => {
    const files = allFiles(ROOT, [], []).filter((f) => !f.dir).length;
    const up = Math.floor((Date.now() - t0) / 1000);
    const accent = st.accent || "cyan";
    const info = [
      [T("lorenzo", "acc", true), T("@"), T("rossi", "acc", true)],
      [T("-------------", "dim")],
      [T("OS", "acc", true), T(": static html5, no frameworks")],
      [T("Host", "acc", true), T(": lorenzoros.si")],
      [T("Kernel", "acc", true), T(": python build.py --build")],
      [T("Uptime", "acc", true), T(`: ${Math.floor(up / 60)} mins, ${up % 60} secs`)],
      [T("Packages", "acc", true), T(`: ${DATA.repos_total} (github), ${Object.keys(DATA.portfolio).length} languages`)],
      [T("Files", "acc", true), T(`: ${files}`)],
      [T("Shell", "acc", true), T(": zsh, allegedly")],
      [T("Font", "acc", true), T(": JetBrains Mono")],
      [T("Theme", "acc", true), T(`: dark, always (accent ${accent})`)],
      [T("Job", "acc", true), T(": software engineer @ CERN")],
      [],
      [T("███", "cyan"), T("███", "green"), T("███", "amber"), T("███", "magenta"), T("███", "dim"), T("███", "fg")],
    ];
    return { ok: true, lines: info.map((segs, i) => ({ segs: [T(`  ${pad(LOGO[i] || "", 20)}`, "acc", true), ...segs] })) };
  };

  const cmdRmRf = (entry) => {
    const files = allFiles(ROOT, [], []);
    const lines = files.map((f) => txt(`${f.dir ? "removed directory" : "removed"} '${f.p}'`, "dim"));
    lines.push(txt(""), txt(`rm: ${files.length} entries removed. the website is gone.`));
    const end = [
      txt(""),
      txt("...just kidding. it's static html: the server keeps a copy, and so does GitHub."),
      line(T("everything is still here: ", "dim"), C("ls", "ls", "acc")),
    ];
    let i = 0;
    if (st.stream) clearInterval(st.stream);
    st.stream = setInterval(() => {
      const done = i >= lines.length;
      printTo(entry, done ? end : lines.slice(i, i + 4));
      i += 4;
      if (!st.editor && !st.app) scrollDown();
      if (done) {
        clearInterval(st.stream);
        st.stream = null;
      }
    }, 30);
    return { ok: true, lines: [] };
  };

  const HELP = [
    ["ls [-la] [dir]", "list a directory"],
    ["cd <dir>", "move around (cd .. goes back)"],
    ["cat <file>", "print a file (also less, head)"],
    ["vi <file>", "open a file in vi, :q to quit"],
    ["nano <file>", "open a file in nano, ctrl+x to exit"],
    ["open <file>", "launch a project, or open a link"],
    ["tree [dir]", "the whole tree at once"],
    ["pwd, whoami, date, echo, history, clear", ""],
  ];

  const cmdHelp = () => {
    const lines = [txt("commands", "acc")];
    for (const [c, d] of HELP) lines.push(line(T(`  ${pad(c, 18)}`), T(d, "dim")));
    lines.push(txt(""), txt("also installed", "acc"));
    const segs = [T("  ")];
    ["neofetch", "htop", "top", "matrix", "corgi", "decimalclock", "enigma hello"].forEach((c, i) => {
      if (i) segs.push(T("  "));
      segs.push(C(c, c));
    });
    lines.push({ segs }, txt(""), txt("tab completes names, ↑ ↓ walk the history, ctrl+l clears.", "dim"));
    return { ok: true, lines };
  };

  const run = (part, entry) => {
    const tok = part.split(/\s+/).filter(Boolean);
    const [name, ...args] = tok;
    if (!name) return { ok: true, lines: [] };
    if (name.startsWith("./")) return cmdOpen([name.slice(2)]);
    switch (name) {
      case "help":
        return cmdHelp();
      case "ls":
      case "dir":
        return cmdLs(args);
      case "ll":
        return cmdLs(["-l", ...args]);
      case "cd": {
        const r = resolve(cwd, args[0] || "~");
        if (r.err) return { ok: false, lines: [txt(`cd: no such file or directory: ${args[0]}`)] };
        if (r.node.type !== "dir") return { ok: false, lines: [txt(`cd: not a directory: ${args[0]}`)] };
        cwd = r.path;
        return { ok: true, lines: [] };
      }
      case "pwd":
        return { ok: true, lines: [txt(`/home/lorenzo${cwd.length ? `/${cwd.join("/")}` : ""}`)] };
      case "cat":
      case "less":
      case "more":
      case "head":
      case "bat":
        return cmdCat(name, args);
      case "vi":
      case "vim":
      case "nvim":
      case "view":
        return cmdEdit("vi", name, args);
      case "nano":
      case "pico":
        return cmdEdit("nano", name, args);
      case "emacs":
        return { ok: false, lines: [txt("zsh: command not found: emacs"), txt("vi and nano are installed. pick a side.", "dim")] };
      case "open":
      case "xdg-open":
        return cmdOpen(args);
      case "tree":
        return cmdTree(args);
      case "clear":
        return { ok: true, clear: true, lines: [] };
      case "whoami":
        return { ok: true, lines: [txt("lorenzo")] };
      case "echo":
        return { ok: true, lines: [txt(args.join(" "))] };
      case "date":
        if (args[0] === "+%decimal") return run("decimalclock", entry);
        return { ok: true, lines: [txt(new Date().toString())] };
      case "decimalclock": {
        const real = DATA.interactive.find((r) => r.name === "decimalclock");
        const lines = [
          line(T("decimal time  ", "dim"), T(decimalTime(new Date()), "acc", true)),
          txt("10 hours a day, 100 minutes an hour, 100 seconds a minute.", "dim"),
        ];
        if (real) lines.push(line(T("the real one: ", "dim"), C("open ~/interactive/decimalclock.url", "open ~/interactive/decimalclock.url")));
        return { ok: true, lines };
      }
      case "enigma":
        if (!args.length) return { ok: false, lines: [txt("usage: enigma <text>", "dim")] };
        return {
          ok: true,
          lines: [
            txt(enigma(args.join(" ")), "acc"),
            txt("rotors I II III · reflector B · start AAA. run it on the output to decode.", "dim"),
            line(T("the full machine: ", "dim"), Lk("github.com/lorossi/pynigma", "https://github.com/lorossi/pynigma")),
          ],
        };
      case "corgi":
        return {
          ok: true,
          lines: CORGI.map((l) => txt(l)).concat([
            txt(""),
            line(T("free delivery of more corgis: ", "dim"), Lk("t.me/corgos_bot", "https://t.me/corgos_bot")),
          ]),
        };
      case "neofetch":
      case "fastfetch":
        return cmdNeofetch();
      case "matrix":
      case "cmatrix":
      case "top":
      case "htop":
      case "sl":
        pendingApp = name;
        return { ok: true, lines: [] };
      case "ssh":
        return {
          ok: true,
          lines: [txt(`ssh: connecting to ${args[0] || "lorenzoros.si"}...`, "dim"), txt("you're already here."), txt("(look up)", "dim")],
        };
      case "history":
        return { ok: true, lines: st.hist.map((h, i) => line(T(`${lpad(i + 1, 4)}  `, "dim"), C(h, h))) };
      case "sudo":
        if (args[0] === "rm") return run(args.join(" "), entry);
        return { ok: false, lines: [txt("lorenzo is not in the sudoers file. This incident will be reported.")] };
      case "rm": {
        const flags = args.filter((a) => a.startsWith("-")).join("");
        if (flags.includes("r") && flags.includes("f")) return cmdRmRf(entry);
        const target = args.find((a) => !a.startsWith("-")) || "";
        return { ok: false, lines: [txt(`rm: cannot remove '${target}': Read-only file system`)] };
      }
      case "mv":
      case "cp":
      case "touch":
      case "mkdir":
      case "chmod":
        return { ok: false, lines: [txt(`${name}: read-only file system`)] };
      case "man":
        return { ok: false, lines: [line(T("What manual page do you want? try "), C("help", "help", "acc"))] };
      case "exit":
      case "logout":
        return {
          ok: true,
          lines: [
            txt("logout"),
            txt("Connection to lorenzoros.si closed. (not really, you're still here)", "dim"),
            line(T("the regular website: ", "dim"), Lk("lorenzoros.si", "/")),
          ],
        };
      default:
        return { ok: false, lines: [txt(`zsh: command not found: ${name}`)] };
    }
  };

  const exec = (raw) => {
    const text = (raw || "").trim();
    const before = dispPath(st.cwd);
    input.value = "";
    st.hIdx = null;
    if (!text) {
      newEntry(before, "");
      scrollDown();
      return;
    }
    st.hist.push(text);
    st.count++;
    cwd = st.cwd.slice();
    pendingEditor = null;
    pendingApp = null;
    const entry = newEntry(before, text);
    let clear = false;
    for (const part of text.split("&&")) {
      const res = run(part.trim(), entry);
      printTo(entry, res.lines);
      if (res.clear) clear = true;
      if (!res.ok) break;
    }
    if (clear) out.replaceChildren();
    st.cwd = cwd;
    refreshChrome();
    scrollDown();
    if (pendingEditor) openEditor(pendingEditor);
    else if (pendingApp) {
      const size = screenSize();
      if (pendingApp === "matrix" || pendingApp === "cmatrix") startMatrix(size);
      else if (pendingApp === "sl") startSl(size);
      else startTop(size, pendingApp === "htop");
    }
  };

  const complete = () => {
    const toks = input.value.split(" ");
    const last = toks[toks.length - 1];
    let matches;
    let apply;
    let base = last;
    if (toks.length === 1) {
      matches = COMMANDS.filter((c) => c.startsWith(last));
      apply = (m, full) => m + (full ? " " : "");
    } else {
      const cut = last.lastIndexOf("/");
      const dirPart = cut >= 0 ? last.slice(0, cut + 1) : "";
      base = last.slice(cut + 1);
      const r = resolve(st.cwd, dirPart);
      if (r.err || r.node.type !== "dir") return;
      matches = sorted(r.node).filter((k) => k.startsWith(base));
      apply = (m, full) => dirPart + m + (full ? (r.node.children[m].type === "dir" ? "/" : " ") : "");
    }
    if (!matches.length) return;
    if (matches.length === 1) {
      toks[toks.length - 1] = apply(matches[0], true);
      input.value = toks.join(" ");
      return;
    }
    let pre = matches[0];
    for (const m of matches) while (!m.startsWith(pre)) pre = pre.slice(0, -1);
    if (pre.length > base.length) {
      toks[toks.length - 1] = apply(pre, false);
      input.value = toks.join(" ");
      return;
    }
    const segs = [];
    matches.forEach((m, i) => {
      if (i) segs.push(T("  "));
      segs.push(T(m, "dim"));
    });
    printTo(newEntry(dispPath(st.cwd), input.value), [{ segs }]);
    scrollDown();
  };

  const konami = (key) => {
    st.kseq.push(key.length === 1 ? key.toLowerCase() : key);
    if (st.kseq.length > 10) st.kseq.shift();
    if (st.kseq.join(",") !== KONAMI) return false;
    st.kseq = [];
    const next = ACCENTS[(ACCENTS.indexOf(st.accent || "cyan") + 1) % ACCENTS.length];
    st.accent = next;
    document.documentElement.style.setProperty("--accent", `var(--accent-${next})`);
    input.value = "";
    printTo(newEntry(null), [
      line(T("↑ ↑ ↓ ↓ ← → ← → B A", next, true)),
      line(T("+30 lives. accent is now ", "dim"), T(next, next, true), T(".", "dim")),
    ]);
    scrollDown();
    return true;
  };

  // ---------- events ----------

  input.addEventListener("keydown", (e) => {
    if (konami(e.key)) {
      e.preventDefault();
      return;
    }
    const h = st.hist;
    if (e.key === "Enter") {
      e.preventDefault();
      exec(input.value);
    } else if (e.key === "Tab") {
      e.preventDefault();
      complete();
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      if (!h.length) return;
      st.hIdx = st.hIdx === null ? h.length - 1 : Math.max(0, st.hIdx - 1);
      input.value = h[st.hIdx];
    } else if (e.key === "ArrowDown") {
      e.preventDefault();
      if (st.hIdx === null) return;
      st.hIdx++;
      if (st.hIdx >= h.length) {
        st.hIdx = null;
        input.value = "";
      } else input.value = h[st.hIdx];
    } else if (e.ctrlKey && e.key.toLowerCase() === "l") {
      e.preventDefault();
      out.replaceChildren();
    } else if (e.ctrlKey && e.key.toLowerCase() === "c" && !String(window.getSelection())) {
      e.preventDefault();
      newEntry(dispPath(st.cwd), `${input.value}^C`);
      input.value = "";
      st.hIdx = null;
      scrollDown();
    }
  });

  // click any command, in the output or in the nav
  document.addEventListener("click", (e) => {
    const target = e.target.closest("[data-cmd]");
    if (!target) return;
    e.preventDefault();
    if (st.app) stopApp();
    if (st.editor) closeEditor();
    exec(target.dataset.cmd);
    focus(input);
  });

  // clicking the terminal focuses the prompt, unless some text is selected
  sh.addEventListener("mouseup", (e) => {
    if (e.target.closest("button, a") || String(window.getSelection())) return;
    focus(input);
  });
  $("app").addEventListener("mouseup", () => focus($("app-key")));

  $("term-quit").addEventListener("click", () => {
    if (st.app) stopApp();
    else closeEditor();
  });

  const viCmd = $("vi-cmd");
  viCmd.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      e.preventDefault();
      viCmd.value = "";
      return;
    }
    if (e.key !== "Enter") return;
    e.preventDefault();
    const v = viCmd.value.trim();
    viCmd.value = "";
    if ([":q", ":q!", ":qa", ":qa!", ":wq", ":wq!", ":x", "ZZ", "ZQ"].includes(v)) closeEditor();
    else if (v === ":w!") edMsg("E212: Can't open file for writing");
    else if (v.startsWith(":w")) edMsg("E45: 'readonly' option is set (add ! to override)");
    else if (["i", "a", "o", "I", "A", "O"].includes(v)) edMsg("-- INSERT -- not today: this file is read-only. :q to quit");
    else if (v === ":help" || v === ":h") edMsg("type :q and press Enter. everyone has been there.");
    else if (v.startsWith(":")) edMsg(`E492: Not an editor command: ${v.slice(1)}`);
    else edMsg("type :q and press Enter to quit");
  });

  const NANO = {
    exit: closeEditor,
    write: () => edMsg("[ File is read-only ]"),
    cut: () => edMsg("[ Read-only file, nothing to cut ]"),
    help: () => edMsg("[ ^X exits. that is all the help there is ]"),
  };
  $("nano-key").addEventListener("keydown", (e) => {
    const k = e.key.toLowerCase();
    if (e.ctrlKey && (k === "x" || k === "o" || k === "k" || k === "g")) {
      e.preventDefault();
      NANO[{ x: "exit", o: "write", k: "cut", g: "help" }[k]]();
    } else if (e.key.length === 1 || e.key === "Backspace" || e.key === "Enter") {
      e.preventDefault();
      edMsg("[ Read-only file, ^X to exit ]");
    }
  });
  $("nano").addEventListener("click", (e) => {
    const b = e.target.closest("[data-nano]");
    if (b) NANO[b.dataset.nano]();
    if (st.editor) focus($("nano-key"));
  });

  $("app-key").addEventListener("keydown", (e) => {
    if (!st.app || e.key === "Tab") return;
    const k = st.app.kind;
    if (k === "matrix") {
      e.preventDefault();
      stopApp();
    } else if (k === "top" && (e.key.toLowerCase() === "q" || e.key === "Escape" || (e.ctrlKey && e.key.toLowerCase() === "c"))) {
      e.preventDefault();
      stopApp();
    } else if (k === "sl") e.preventDefault(); // sl ignores you, as it should
  });

  // ---------- boot ----------

  const now = new Date();
  printTo(newEntry(null), [
    txt(`Last login: ${now.toDateString()} ${now.toTimeString().slice(0, 5)} on ttys001`, "dim"),
    txt(""),
    line(T("type "), C("help", "help", "acc"), T(" for the commands, or click any name to open it.")),
    txt(""),
  ]);
  input.placeholder = "type help, or try: cd portfolio";
  exec("ls");
  st.hist = ["ls"];
  input.addEventListener("input", () => {
    input.placeholder = "";
  });
})();
