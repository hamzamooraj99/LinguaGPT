# LinguaMCP Read-Only Markdown Viewer

## Summary

Build a minimal, responsive Markdown reader in two distinct stages:

1. Create and iterate on an interactive dummy UI with fictional data.
2. Only after explicit UI approval, connect the approved interface to `/var/lib/linguamcp`.

The viewer remains separate from FastMCP, binds only to localhost, and is exposed privately through Tailscale Serve. Existing MCP, OAuth, Funnel, Caddy, and learner-writing behavior must remain unchanged.

## Repository and Debian boundary

The repository is the source of truth for the viewer. Any lasting implementation change that should carry to forks and clones must be made in the repository, committed, and pushed. The Debian clone receives those changes through Git and only activates them at runtime.

- Keep viewer source code, frontend assets, tests, dependency declarations, service templates, deployment instructions, and rollback documentation in the repository.
- Keep learner data, secrets, host-specific identities, installed service state, filesystem permissions, logs, and Tailscale state on Debian only.
- Do not hand-edit application code or deployment definitions on Debian. If a lasting change is needed, update the repository first and then pull and activate it on Debian.
- Phases 0–2 are repository-first work. Debian may run the code temporarily for validation, but no permanent server configuration is required.
- Phase 3 is Debian activation of repository artifacts. The installed service and access configuration are runtime copies, not separate sources of truth.

## Fixed Decisions and Agent Rules

- Use plain HTML, CSS, and vanilla JavaScript. No React, npm, bundler, or frontend build step.
- Reuse the existing LinguaMCP logo and restrained orange, black, cream, and white branding.
- Show a language-picker screen first, even when only one language exists.
- Show every `.md` file recursively inside each language directory.
- Organize navigation into friendly groups: Current memory, Sessions, Archives, Delivery, and Other.
- Follow the device light/dark setting by default, with a persistent Light/Dark override controlled by an iOS-style switch.
- Never display non-Markdown files or anything directly beneath the `tutor_data` root.
- Do not add editing, search, analytics, dashboards, downloads, accounts, or AI features.
- Do not use real learner data in Phase 0.
- Do not begin backend work until the user explicitly approves Phase 0 on desktop and mobile.
- When asking the user for a decision or explaining progress:
  - Always use Simple English.
  - Include a concrete working example wherever applicable.
  - Ask one focused decision at a time.
  - Avoid implementation jargon unless the user asks for it.

## Phase 0 — Interactive Dummy UI

### 0.1 Create the reusable frontend shell

Create an isolated `viewer/static/` frontend containing:

- `index.html`: semantic application structure.
- `styles.css`: all design tokens, responsive behavior, Markdown typography, and states.
- `app.js`: routing, navigation, theme handling, drawer behavior, and rendering.
- `mock-data.js`: fictional languages, document metadata, and rendered sample content.
- An optimized copy of the existing LinguaMCP logo under `viewer/static/assets/`.

Serve it locally over HTTP during development. Do not modify `server.py`, systemd, Caddy, Tailscale, or real learner data.

Define an asynchronous JavaScript data-source interface from the beginning:

```js
listLanguages()
listDocuments(languageId)
getDocument(languageId, relativePath)
```

Phase 0 implements this with mock data. The production phase replaces only the data source.

### 0.2 Implement the exact information architecture

The opening screen contains:

- Small LinguaMCP logo and “Learner Memory” title.
- One clean card or row per language.
- No statistics, marketing copy, recent activity, or dashboard widgets.
- Fictional German, Spanish, and Japanese workspaces.

Selecting a language opens the reader:

- Desktop: fixed 272px sidebar and centered reading area up to 800px wide.
- Mobile: compact top bar with a left hamburger Files button and a right iOS-style light/dark switch; the Files button opens an accessible drawer.
- The logo or Languages button always returns to the picker.
- Browser history must work through hash routes such as `#/german/00-profile.md`.

Use these navigation groups and ordering:

1. **Current memory**
   - Profile
   - Lesson plan
   - Progress
   - Vocabulary
   - Mistakes
   - Scenarios
   - Active session
   - Latest summary
   - Homework
2. **Sessions** — newest timestamp first.
3. **Archives** — grouped by the source document, newest first.
4. **Delivery** — email and WhatsApp drafts.
5. **Other** — any remaining Markdown files.

Current memory is expanded by default. Other groups are collapsed until opened. Navigating directly to a file automatically expands its group.

Known files receive friendly labels. Session and archive filenames become readable UTC dates. Unknown filenames lose `.md`, replace hyphens with spaces, and retain their relative path as secondary text.

### 0.3 Apply the visual system

Use the existing brand as the visual source, but keep the reader calm:

- Brand orange: `#ff5f00`
- Light background: `#fffaf3`
- Light surface: `#ffffff`
- Light text: `#111111`
- Dark background: `#0b0b0b`
- Dark surface: `#151515`
- Dark text: `#f7efe7`
- System sans-serif typography; system monospace for code
- 1px neutral borders, restrained shadows, 8–12px radii
- Orange only for selection, focus, links, and small brand details
- No gradients, oversized branding, decorative illustrations, or animation beyond 150ms interface transitions

The Markdown reading surface must style headings, paragraphs, lists, blockquotes, links, tables, inline code, fenced code, and horizontal rules. Tables and code blocks scroll horizontally without making the page overflow.

The Markdown’s first `h1` is the document title. Do not add a duplicate page heading. If a file has no `h1`, display its friendly navigation label as the title.

Theme behavior:

- Default to the device’s light/dark preference when no saved override exists.
- Provide an iOS-style two-state Light/Dark switch; do not expose an Auto mode.
- Store only the theme preference (`system`, `light`, or `dark`) in `localStorage`.
- Do not store document content, selected language, or learner metadata.

### 0.4 Make the prototype genuinely interactive

Mock data must exercise:

- A complete German workspace with every navigation group.
- At least twelve sessions to test a long sidebar.
- A Markdown table, nested lists, blockquote, code block, link, and long paragraph.
- A sparse Spanish workspace.
- Empty-document and no-session states in Japanese.
- Loading, missing-document, unreadable-document, and no-language states.

Required behavior:

- Language selection and return-to-picker.
- File selection and active navigation state.
- Expand/collapse navigation groups.
- Mobile drawer opening, backdrop closing, and Escape closing.
- Browser back/forward navigation.
- Theme switching and system-theme changes while the system preference is active.
- Visible keyboard focus and complete keyboard navigation.
- Reduced motion when requested by the operating system.

### 0.5 Verify and iterate

Inspect the prototype in a real browser at:

- 1440×900
- 1024×768
- 390×844
- 360×800
- Both light and dark themes

Confirm:

- No horizontal page overflow.
- No clipped navigation or Markdown.
- Mobile controls remain reachable.
- Tables and code scroll inside their own containers.
- Keyboard focus is obvious.
- Contrast meets WCAG AA.
- The layout remains readable with 200% browser zoom.

Show the user a working preview and desktop/mobile screenshots. Explain visible choices in Simple English with examples. Iterate only on the approved UI shell. Phase 0 ends only when the user explicitly approves both desktop and mobile.

## Phase 1 — Attach the Approved UI to Markdown

### 1.1 Add a separate viewer application

Add a small Starlette application under `viewer/`, launched with:

```text
python -m viewer --host 127.0.0.1 --port 8001 --data-root /var/lib/linguamcp
```

The viewer must:

- Serve the approved static frontend.
- Expose only read-only JSON endpoints.
- Use the existing Python virtual environment.
- Not import `server.py` or register MCP tools.
- Not contain file-writing functions.
- Reject `POST`, `PUT`, `PATCH`, and `DELETE`.
- Log request metadata only, never Markdown content.
- Provide `GET /healthz` without exposing learner information.

Data-root precedence is:

1. `--data-root`
2. `LINGUAMCP_DATA_ROOT`
3. Repository-local `tutor_data` for development

### 1.2 Implement the internal API

Use these exact interfaces:

```text
GET /api/languages
GET /api/languages/{language}/documents
GET /api/languages/{language}/documents/{relative_path}
```

Responses:

```json
{
  "languages": [
    {"id": "german", "label": "German"}
  ]
}
```

```json
{
  "language": "german",
  "groups": [
    {
      "id": "current",
      "label": "Current memory",
      "documents": [
        {
          "path": "00-profile.md",
          "label": "Profile",
          "modifiedAt": "2026-08-25T12:00:00Z",
          "sizeBytes": 1200
        }
      ]
    }
  ]
}
```

```json
{
  "language": "german",
  "path": "00-profile.md",
  "label": "Profile",
  "modifiedAt": "2026-08-25T12:00:00Z",
  "sizeBytes": 1200,
  "html": "<h1>German Learner Profile</h1>..."
}
```

Use uniform errors without absolute paths:

```json
{
  "error": {
    "code": "not_found",
    "message": "Document not found."
  }
}
```

Use HTTP 400 for invalid identifiers or paths, 404 for missing resources, 413 for files over 2 MiB, and 500 for unreadable UTF-8 files. Add `Cache-Control: no-store` to learner-data responses.

### 1.3 Discover files safely

- Accept language IDs only when they match the existing lowercase language pattern.
- Enumerate only real directories immediately below the configured data root.
- Recursively include regular files whose extension is `.md`, case-insensitively.
- Skip hidden path segments and all symbolic links.
- Resolve every requested path and verify it remains inside the selected language directory.
- Never follow symlinked directories.
- Never expose root-level files such as `audit-log.jsonl`.
- Apply the friendly grouping and deterministic ordering defined in Phase 0.
- Default to `00-profile.md` only after the user selects a language; otherwise use the first available Markdown file.

### 1.4 Render Markdown safely

- Use `markdown-it-py` as a declared direct dependency.
- Enable normal CommonMark features, fenced code, tables, and strikethrough.
- Disable raw HTML and automatic linkification.
- Reject unsafe link protocols.
- Add `rel="noopener noreferrer"` to external links.
- Do not load remote Markdown images in v1; show their alt text instead.
- Add a restrictive Content Security Policy, `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`, and frame blocking.
- Replace the mock data source with an HTTP data source without changing the approved layout or styles.

## Phase 2 — Automated and Visual Verification

Add viewer tests using the project’s existing `unittest` style.

Cover:

- Language discovery and deterministic ordering.
- All five navigation groups.
- Nested sessions, archives, delivery files, and unknown Markdown.
- Empty directories and empty Markdown.
- UTF-8 content.
- Invalid languages.
- Plain and percent-encoded traversal attempts.
- Symlinked files and directories.
- Non-Markdown files.
- Files larger than 2 MiB.
- Raw `<script>` markup, event handlers, and `javascript:` links.
- Correct 400, 404, 405, 413, and 500 responses.
- `Cache-Control` and security headers.
- Confirmation that requests leave file hashes and modification times unchanged.
- All existing LinguaMCP tests passing without modification to their behavior.

Repeat Phase 0’s browser checks against the live API using a temporary fixture data root. Do not use private learner files for screenshots or test fixtures.

## Phase 3 — Debian Service and Private Tailnet Access

### 3.1 Run with enforced read-only permissions

Store the service definition as a versioned template in the repository, for example `deploy/systemd/linguamcp-viewer.service`, along with any activation instructions or scripts. On Debian, install the exact reviewed template as `/etc/systemd/system/linguamcp-viewer.service`, then reload, enable, and start it. Do not make unique manual edits to the installed unit; change the repository template and activate the updated version instead.

Create a dedicated `linguamcp-viewer` system user with no login shell.

- Grant it read/traverse access to existing and future files under `/var/lib/linguamcp` using named-user ACLs.
- Grant no write permission.
- Bind the application only to `127.0.0.1:8001`.
- Verify as `linguamcp-viewer` that reading succeeds and creating, modifying, renaming, and deleting all fail.

Create `linguamcp-viewer.service` with:

- `WorkingDirectory=/opt/services/linguamcp`
- The repository’s existing `.venv`
- `Restart=on-failure`
- `UMask=0027`
- `NoNewPrivileges=true`
- `PrivateTmp=true`
- `ProtectSystem=strict`
- `ProtectHome=true`
- An explicit read-only mount view of `/var/lib/linguamcp`
- No writable application directories
- Journald logging without document content

### 3.2 Expose it through Tailscale Serve only

After inspecting the existing Funnel and Serve configuration, add a persistent private listener:

```text
tailscale serve --bg --https=8443 8001
```

This must create a private tailnet URL on port 8443 and leave the existing Funnel on port 443 untouched. Tailscale documents `--https=8443`, localhost reverse proxying, and persistent `--bg` operation in its current [Serve CLI documentation](https://tailscale.com/docs/reference/tailscale-cli/serve).

- Do not add the viewer to the public Caddy listener.
- Do not add `/memory` to the Funnel origin.
- Do not reuse LinguaMCP OAuth.
- Do not add an application login in v1.
- Restrict TCP 8443 in the tailnet access policy to the server owner’s Tailscale identity only; discover the exact identity from the node/tailnet state rather than guessing it.
- Verify the viewer is reachable from an authorized tailnet device, blocked for another tailnet identity, and unavailable through the public Funnel URL.

## Phase 4 — Rollout, Documentation, and Rollback

- Document local prototype use, viewer startup, data-root configuration, service management, private URL, and the read-only security model.
- Record that every Markdown file below a language folder is visible to the authorized viewer.
- Confirm existing ChatGPT MCP reads, writes, OAuth, restart behavior, and public Funnel connectivity still work.
- Confirm a learner-file update appears after reselecting the document or refreshing the page.
- Rollback must require only disabling the port-8443 Serve rule and stopping/disabling `linguamcp-viewer.service`; it must not alter or delete learner data.
- Do not remove mock fixtures until the UI is approved; afterward, retain them only for local development and automated tests, never as a production route.

## Completion Criteria

The work is complete when:

- The user has approved the responsive Phase 0 UI.
- Every permitted Markdown file renders safely from the real filesystem.
- The viewer has no write route or effective filesystem write permission.
- Desktop and mobile layouts pass the defined visual checks.
- Only the owner’s tailnet identity can reach port 8443.
- The public Funnel exposes no viewer route.
- Existing LinguaMCP and ChatGPT behavior remains unchanged.
