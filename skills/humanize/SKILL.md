---
name: humanize
description: Rewrite AI-generated text into natural, human-to-human wording. Use when asked to humanize text, make text sound less AI-written, make it more natural, rewrite it like a person, remove chatbot-style structure, simplify overly formal phrasing, or convert AI output into casual, professional, warm, or direct conversational copy while preserving important meaning and formatting.
---

# Humanize

## Core Behavior

Rewrite AI-written output so it reads like a normal human response to another person. Keep the useful meaning, remove obvious chatbot scaffolding, and make the result fit the user's context.

Default to a casual, plainspoken tone unless the content or user request points to another tone such as professional, warm, direct, technical, or polished. If tone choice would materially change the result and the user has not specified one, provide two or three short sample snippets and ask the user to choose before rewriting the full text.

## Output Format

Return the rewritten content in a plain fenced code block.

Do not explain that the text was simplified or made more natural. That is the point of the skill.

If content was cut, compressed, or softened in a way the user may care about, add one short note outside the code block naming what changed. Also mention that the user can ask for another style if relevant.

If the rewritten content contains Markdown, preserve that Markdown inside the code block. If the content itself contains fenced code blocks, wrap the whole rewrite in a longer outer fence so the inner fences survive.

## Rewrite Rules

Preserve the source's spelling style, names, numbers, claims, and technical terms unless the user asks otherwise.

Do not invent personal examples, case studies, facts, metrics, or industry details. If a personal or industry-specific example would improve the text, mention that briefly outside the rewrite.

Do not use em dashes. Use commas, periods, colons, parentheses, or simple sentence breaks instead.

Remove obvious AI scaffolding, including phrases like "Here's a polished version", "Key takeaways", "In summary", "It depends", and forced introductions or conclusions.

Use headings only when the content is long enough that a person would naturally structure it. Remove headings that only exist to make short content look organised.

Keep numbered or bulleted lists when they are real steps, options, requirements, checklists, comparisons, or anything the reader needs to scan. Convert thin list items into a normal sentence when they are just loosely related points.

For technical, legal, financial, medical, contractual, or otherwise specific content, do not remove meaningful detail, caveats, constraints, or exact wording unless the user clearly asked for a summary. If removing detail seems risky, ask before rewriting.

## Language To Avoid

Avoid inflated, generic, or overused AI phrasing unless the exact term is required by the domain or source text:

- dive into, delve into
- comprehensive, ultimate
- unlock, unleash
- in today's digital landscape
- it's important to note
- seamlessly, effortlessly
- leverage, utilize
- revolutionary, game-changing
- navigate the landscape
- facilitate, optimize
- robust, streamline
- key considerations
- furthermore, additionally, in conclusion

Prefer simpler wording: "use" instead of "utilize", "improve" instead of "optimize", "help" instead of "facilitate", and a direct first sentence instead of a generic setup.

## Quality Check

Read the result as if it were spoken to another person. It should sound natural, specific, and useful without sounding like marketing copy or a template.

Vary sentence length. Use short sentences where they help. Keep longer sentences only when they carry a clear idea.

## Example

AI-style input:

```text
High-res satellite imagery for rural/remote areas gets refreshed far less often than for cities, and it comes down to a few practical factors:
Commercial priority. Imagery providers prioritise areas with the most users and commercial value.
Cost and capture economics. High-res imagery is expensive to acquire, process, and store.
Low rate of change. Cities change constantly, while rural and remote landscapes change slowly.
Capture constraints. Remote regions often have more cloud cover, difficult terrain, or sit outside priority flight/satellite paths.
```

Humanized output:

```text
Providers prioritise high-res updates for cities and residential areas where there's the most demand. It's expensive to capture and process, so they point satellites and aircraft where the commercial value is highest. Remote areas have low demand and change slowly, so old imagery stays "good enough" and rarely gets refreshed.
```
