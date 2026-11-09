# Pandeomonium: guide for agents

Pandeomonium is a noir-absurdist comic published at
<https://pandeomonium.debedb.com> (WordPress.com). This repo holds the issue
tracker, the tooling that generates and publishes strips, and this guide. The
name is *pandemonium* with a *daemon* in it, and *pantheon* close by.

## Ethos

- **The question.** Above everything sits "Are we communicating?" That is why
  John Searle is here, starving for Chinese food.
- **Who is in charge.** Under that question, humans think they run things, but
  maybe they don't. The quiet powers are R. Daneel and R. Giskard, the cats, the
  owls, and Woland. The question keeps twisting and is never settled. No
  character settles it, there is no finale, and nothing builds toward an
  ending. "Because there is none."
- **Never over-explain.** Don't explain the jokes, in the strip or in
  discussion. Song quotes, film lines and allusions go unspoken unless the
  issue says a character speaks them. Titles and captions are minimal.
- **Irreverent, not cruel.** The series is deliberately irreverent about gods,
  prophets, philosophers and pop culture. The absurdity is in the situation.
  It never lands on real grief: when an artist sings a lament, draw them
  singing it in earnest, and no punchline undercuts the song. Consolation is
  given, not used as an interruption. When the material turns melancholic, let
  the strip turn melancholic. "We don't just shit on genuine emotions."
- **Check the history.** Before a punchline rests on a quote or anecdote, verify
  it (e.g. *credo quia absurdum* is a later paraphrase of Tertullian). For a
  Russian-language reference, check the Russian original before you "correct"
  it from English.
- **Real people get drawn with care.** Likenesses should be recognizable. Use the
  reference images the issue names.
- **Continuity.** A recurring character looks the same in every strip. The R's
  look fully human and are only "merely present"; only subtle behaviours give
  them away. Rabbi Joshua, Kant, Landa (Christoph Waltz) and the rest keep their
  established likeness, costume and props from panel to panel and from strip to
  strip. Keep props and costumes consistent inside a strip too: a character
  doesn't lose a coat between panels.
- **Point of view.** When a character reads or discovers something, draw it over
  their shoulder so the reader sees what they see.
- **Arcs cross.** Arcs intersect over and over again. Between-arc interjections
  in the Gilliam / Monty Python manner ("Anyway." / "Who said that?") are fine,
  but the comic has its own ethos, not Gilliam's. Arc markers are undecided.
- **Timelines jump.** Strips go back and forth between arcs and timelines with
  no bridging. A new strip can pick up any earlier thread right away, and
  readers will place it.
- **The author is a stick figure.** When the wall breaks and characters reach
  the person drawing them, the author appears as a crude stick figure with a
  pencil and sketchpad. That figure is the author-function, not a person, and
  it is the only thing on the page drawn in that register. Terry Gilliam and
  Monetochka are meta layers *inside* the comic, drawn like any other
  character; they are not the author.
- **Locally defensible, globally insane.** Every transition makes sense on its
  own terms, even when the overall topology is absurd. The humor comes from
  precise compliance with the wrong layer of a request.
- **Liberties are deliberate.** When the author takes a liberty with canon
  ("R? R."), don't raise it again.

## Workflow

Every new idea follows issue -> worktree -> PR -> artifact:

1. **Issue.** Each strip or arc gets an issue in this repo. The issue holds the
   author's brief (panels, titles, likeness notes) and the discussion. Analyze
   the brief and ask questions before drawing; don't start generating when the
   author asked for analysis first.
2. **Worktree.** Do branch work in `../pandeomonium.worktrees/<branch>/`. The main
   checkout stays on `master`.
3. **PR.** Scripts, prompts and state changes go in a PR that links the issue
   (`Closes #N`). Rendered strips and reference images stay out of git (see
   `.gitignore`).
4. **Artifact: a WordPress draft for review.** The deliverable is a **draft**
   post on pandeomonium.debedb.com. Post its preview link
   (`https://pandeomonium.debedb.com/?p=<id>&preview=true`) on the issue. Never
   publish without explicit approval ("ship it", "publish"). Do one strip at a
   time: a strip is published before the next one is drafted, unless the author
   asks for several at once.
5. **Ship.** On approval: publish the post, add a "next ->" link to the
   previous strip, merge the PR, and close the issue once its strips are out.

## Tooling

- `tools/` holds the generation and publishing scripts (image generation and
  edits via the OpenAI Images API, WordPress.com REST publishing), carried over
  from the earlier setup. They still assume that layout's working directory
  (`.claude/assets/...`), so fix paths in a PR the first time you use one.
  `tools/pandeomonium/state.json` maps strip keys to WP post and media IDs.
- Credentials come from the environment or the macOS Keychain
  (`OPENAI_API_KEY`, Keychain item `wpcom_token` / `WPCOM_TOKEN`). Never write a
  credential into the repo, an issue or a log.
- `media/hq-<n>/` holds images re-hosted from the issues that migrated here
  (`hq-<n>` is the original issue number).

## Don'ts

- Don't publish without approval, and don't publish two strips in one step
  unless asked.
- Don't commit generated strip PNGs, reference photos or logs.
- Don't add an ending, a moral, or an explanation.
