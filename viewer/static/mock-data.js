const coreGroup = (documents) => ({
  id: "current",
  label: "Current memory",
  openByDefault: true,
  documents,
});

const documentEntry = (path, label, group, html, modifiedAt = "2026-08-25T10:00:00Z") => ({
  path,
  label,
  group,
  html,
  modifiedAt,
  sizeBytes: Math.max(320, html.length * 2),
});

const germanCore = [
  documentEntry(
    "00-profile.md",
    "Profile",
    "current",
    `<h1>German Learner Profile</h1>
<p>This profile keeps the durable details that make future lessons feel continuous.</p>
<h2>Goals</h2>
<ul>
  <li>Hold relaxed everyday conversations while travelling.</li>
  <li>Move from A2 toward a confident B1 speaking level.</li>
  <li>Understand German word order without translating every sentence.</li>
</ul>
<h2>Background</h2>
<ul>
  <li>Enjoys short speaking exercises and practical examples.</li>
  <li>Can read simple present-tense German.</li>
  <li>Often hesitates with the perfect tense and separable verbs.</li>
</ul>
<blockquote><p>Keep corrections kind, specific, and immediately useful.</p></blockquote>`,
  ),
  documentEntry(
    "01-lesson-plan.md",
    "Lesson plan",
    "current",
    `<h1>German Lesson Plan</h1>
<h2>Current focus</h2>
<p>Build confidence describing yesterday’s travel plans using the perfect tense.</p>
<h2>Upcoming topics</h2>
<ol>
  <li>Past-tense storytelling with <em>haben</em> and <em>sein</em>.</li>
  <li>Polite requests at a hotel and train station.</li>
  <li>Short listening exercises with natural filler words.</li>
</ol>
<h2>Suggested rhythm</h2>
<p>Start with a two-minute warm-up, move into one roleplay, then finish with three deliberate corrections.</p>`,
  ),
  documentEntry(
    "02-progress.md",
    "Progress",
    "current",
    `<h1>German Progress</h1>
<p>Recent progress is measured by what the learner can do spontaneously, not by a score.</p>
<table><thead><tr><th>Area</th><th>Current signal</th><th>Next step</th></tr></thead><tbody>
<tr><td>Speaking</td><td>Can sustain a two-minute answer.</td><td>Add follow-up questions.</td></tr>
<tr><td>Grammar</td><td>Understands the verb-second pattern.</td><td>Use it under time pressure.</td></tr>
<tr><td>Listening</td><td>Catches familiar phrases.</td><td>Practice reduced speech.</td></tr>
</tbody></table>`,
  ),
  documentEntry(
    "03-vocabulary.md",
    "Vocabulary",
    "current",
    `<h1>German Vocabulary</h1>
<p>Words are kept with a useful example instead of as isolated translations.</p>
<table><thead><tr><th>German</th><th>Meaning</th><th>Example</th></tr></thead><tbody>
<tr><td><strong>umsteigen</strong></td><td>to change trains</td><td>Wir müssen in Köln umsteigen.</td></tr>
<tr><td><strong>zuverlässig</strong></td><td>reliable</td><td>Die Bahn ist heute zuverlässig.</td></tr>
<tr><td><strong>die Fahrkarte</strong></td><td>ticket</td><td>Wo kann ich eine Fahrkarte kaufen?</td></tr>
</tbody></table>
<p><code>umsteigen</code> is a separable verb: <em>Ich steige in Köln um.</em></p>`,
  ),
  documentEntry(
    "04-mistakes.md",
    "Mistakes",
    "current",
    `<h1>German Mistakes</h1>
<h2>Useful corrections</h2>
<ul>
  <li><strong>Ich habe gegangen</strong> → <strong>Ich bin gegangen</strong> for movement with <em>sein</em>.</li>
  <li><strong>weil ich bin müde</strong> → <strong>weil ich müde bin</strong> in a subordinate clause.</li>
</ul>
<h2>Practice cue</h2>
<p>Before answering, pause long enough to place the verb. A short pause is better than restarting the sentence.</p>`,
  ),
  documentEntry(
    "05-scenarios.md",
    "Scenarios",
    "current",
    `<h1>German Scenarios</h1>
<h2>Train station — in progress</h2>
<p>Ask for a platform, confirm a connection, and respond when the train is delayed.</p>
<h2>Hotel check-in — ready</h2>
<p>Explain a reservation problem and ask for a quieter room.</p>`,
  ),
  documentEntry(
    "active-session.md",
    "Active session",
    "current",
    `<h1>German Active Session</h1>
<p><strong>Status:</strong> Warm-up complete; moving into a travel roleplay.</p>
<h2>Topics covered</h2>
<ul><li>Perfect tense with movement verbs.</li><li>Asking for clarification.</li></ul>
<h2>New vocabulary</h2>
<ul><li><strong>die Verspätung</strong> — delay</li></ul>
<h2>Corrections</h2>
<p>Keep the verb at the end after <em>weil</em>.</p>
<h2>Next action</h2>
<p>Roleplay a missed connection without switching to English.</p>`,
    "2026-08-25T09:45:00Z",
  ),
  documentEntry(
    "latest-summary.md",
    "Latest summary",
    "current",
    `<h1>German Latest Session Summary</h1>
<p>We practised explaining a missed train and asking for the next connection.</p>
<h2>Practiced</h2>
<ul><li>Perfect tense with <em>sein</em>.</li><li>Polite questions with <em>Könnten Sie…?</em></li></ul>
<h2>Homework</h2>
<p>Record a one-minute story about a journey that went wrong.</p>
<h2>Next recommended focus</h2>
<p>Repeat the story with three different time expressions.</p>`,
    "2026-08-24T15:30:00Z",
  ),
  documentEntry(
    "latest-homework.md",
    "Homework",
    "current",
    `<h1>German Homework</h1>
<h2>Due</h2>
<p>Before the next session.</p>
<h2>Exercises</h2>
<ol><li>Tell the travel story once slowly.</li><li>Tell it again without notes.</li><li>Underline every verb with <em>sein</em>.</li></ol>
<h2>Optional challenge</h2>
<p>Add one unexpected problem and solve it politely.</p>`,
  ),
];

const germanSessions = [
  ["2026-08-24T15-30-00-000000Z.md", "24 Aug 2026 · Travel problems", "We practised a missed-connection roleplay and reviewed <em>sein</em> in the perfect tense."],
  ["2026-08-18T10-10-00-000000Z.md", "18 Aug 2026 · At the hotel", "We asked for a quieter room, clarified a reservation, and practised polite requests."],
  ["2026-08-12T17-00-00-000000Z.md", "12 Aug 2026 · Directions", "We gave directions with landmarks and corrected word order after <em>weil</em>."],
  ["2026-08-06T09-20-00-000000Z.md", "06 Aug 2026 · Daily routine", "We described a weekday using time phrases and separable verbs."],
  ["2026-07-30T13-40-00-000000Z.md", "30 Jul 2026 · Food order", "We ordered lunch, asked about ingredients, and compared formal and informal language."],
  ["2026-07-22T11-00-00-000000Z.md", "22 Jul 2026 · Making plans", "We made a weekend plan and practised agreeing and disagreeing naturally."],
  ["2026-07-15T16-10-00-000000Z.md", "15 Jul 2026 · Past events", "We built a short story with yesterday, last week, and once before."],
  ["2026-07-08T08-45-00-000000Z.md", "08 Jul 2026 · Listening warm-up", "We listened for familiar chunks and asked for repetition without apologising."],
  ["2026-07-01T14-25-00-000000Z.md", "01 Jul 2026 · Introductions", "We introduced ourselves and described learning goals."],
  ["2026-06-24T10-30-00-000000Z.md", "24 Jun 2026 · First review", "We revisited greetings, questions, and the learner’s preferred correction style."],
  ["2026-06-17T15-00-00-000000Z.md", "17 Jun 2026 · First roleplay", "We practised ordering coffee and asking the other person to slow down."],
  ["2026-06-10T09-00-00-000000Z.md", "10 Jun 2026 · Welcome session", "We set goals, established a simple routine, and created the first lesson plan."],
].map(([filename, label, summary], index) => documentEntry(
  `sessions/${filename}`,
  label,
  "sessions",
  `<h1>${label}</h1><p>${summary}</p><h2>Session note</h2><p>This fictional session demonstrates how a permanent Markdown log reads in the viewer. The source of truth remains the file itself.</p><blockquote><p>One useful correction is better than ten vague ones.</p></blockquote>`,
  `2026-${String(8 - Math.floor(index / 2)).padStart(2, "0")}-${String(24 - index).padStart(2, "0")}T12:00:00Z`,
));

const germanArchives = [
  documentEntry(
    "archives/03-vocabulary/2026-07-01T12-00-00-000000Z.md",
    "Vocabulary · 01 Jul 2026",
    "archives",
    `<h1>Vocabulary archive</h1><p>An older snapshot of the vocabulary file before a careful compaction.</p><ul><li><strong>die Verbindung</strong> — connection</li><li><strong>der Bahnsteig</strong> — platform</li></ul>`,
    "2026-07-01T12:00:00Z",
  ),
  documentEntry(
    "archives/03-vocabulary/2026-06-10T12-00-00-000000Z.md",
    "Vocabulary · 10 Jun 2026",
    "archives",
    `<h1>Vocabulary archive</h1><p>The first vocabulary snapshot from the fictional German workspace.</p><p>Greetings, travel, and simple questions.</p>`,
    "2026-06-10T12:00:00Z",
  ),
];

const germanDelivery = [
  documentEntry(
    "delivery/latest-email.md",
    "Email draft",
    "delivery",
    `<h1>Email Draft</h1><h2>Subject</h2><p>German lesson summary and homework</p><h2>Body</h2><p>Today we practised a travel problem and reviewed the perfect tense.</p>`,
  ),
  documentEntry(
    "delivery/latest-whatsapp.md",
    "WhatsApp draft",
    "delivery",
    `<h1>WhatsApp Draft</h1><p>Heute: eine Reisegeschichte mit <em>sein</em> im Perfekt. Bis bald!</p>`,
  ),
];

const germanOther = [
  documentEntry(
    "notes/reading-list.md",
    "Reading list",
    "other",
    `<h1>Reading List</h1><p>A small fictional note that sits outside the standard memory files.</p><ul><li>Short train announcements</li><li>A2 graded reader</li><li><a href="https://example.com/">A safe example link</a></li></ul>`,
  ),
];

const spanishCore = [
  documentEntry(
    "00-profile.md",
    "Profile",
    "current",
    `<h1>Spanish Learner Profile</h1><h2>Goals</h2><ul><li>Order food with confidence.</li><li>Speak in short, clear sentences.</li></ul><h2>Background</h2><p>This fictional workspace is intentionally sparse so the empty and early-stage states can be reviewed.</p>`,
  ),
  documentEntry(
    "01-lesson-plan.md",
    "Lesson plan",
    "current",
    `<h1>Spanish Lesson Plan</h1><h2>Current focus</h2><p>Greetings, introductions, and useful restaurant phrases.</p>`,
  ),
  documentEntry(
    "03-vocabulary.md",
    "Vocabulary",
    "current",
    `<h1>Spanish Vocabulary</h1><p><strong>la cuenta</strong> — the bill</p>`,
  ),
];

const japaneseCore = [
  documentEntry(
    "00-profile.md",
    "Profile",
    "current",
    `<h1>Japanese Learner Profile</h1><p>This workspace is ready for a future learner profile.</p><h2>Goals</h2><p>No goals recorded yet.</p>`,
  ),
  documentEntry(
    "active-session.md",
    "Active session",
    "current",
    `<h1>Japanese Active Session</h1><p><strong>Status:</strong> No active session checkpoint.</p><p>There is nothing to display here yet.</p>`,
  ),
];

const workspaces = {
  german: {
    id: "german",
    label: "German",
    groups: [
      coreGroup(germanCore),
      { id: "sessions", label: "Sessions", openByDefault: false, documents: germanSessions },
      { id: "archives", label: "Archives", openByDefault: false, documents: germanArchives },
      { id: "delivery", label: "Delivery", openByDefault: false, documents: germanDelivery },
      { id: "other", label: "Other", openByDefault: false, documents: germanOther },
    ],
  },
  spanish: {
    id: "spanish",
    label: "Spanish",
    groups: [
      coreGroup(spanishCore),
      { id: "sessions", label: "Sessions", openByDefault: false, documents: [] },
      { id: "archives", label: "Archives", openByDefault: false, documents: [] },
      { id: "delivery", label: "Delivery", openByDefault: false, documents: [] },
      { id: "other", label: "Other", openByDefault: false, documents: [] },
    ],
  },
  japanese: {
    id: "japanese",
    label: "Japanese",
    groups: [
      coreGroup(japaneseCore),
      { id: "sessions", label: "Sessions", openByDefault: false, documents: [] },
      { id: "archives", label: "Archives", openByDefault: false, documents: [] },
      { id: "delivery", label: "Delivery", openByDefault: false, documents: [] },
      { id: "other", label: "Other", openByDefault: false, documents: [] },
    ],
  },
};

const clone = (value) => JSON.parse(JSON.stringify(value));

export const mockDataSource = {
  async listLanguages() {
    await new Promise((resolve) => setTimeout(resolve, 90));
    return Object.values(workspaces).map(({ id, label }) => ({ id, label }));
  },

  async listDocuments(languageId) {
    await new Promise((resolve) => setTimeout(resolve, 90));
    const workspace = workspaces[languageId];
    if (!workspace) throw new Error("language_not_found");
    return clone(workspace.groups);
  },

  async getDocument(languageId, relativePath) {
    await new Promise((resolve) => setTimeout(resolve, 120));
    const workspace = workspaces[languageId];
    const document = workspace?.groups.flatMap((group) => group.documents).find(({ path }) => path === relativePath);
    if (!document) throw new Error("document_not_found");
    return clone({ language: workspace.label, ...document });
  },
};
