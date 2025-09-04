
Voice-to-Slide Generator

  Description: Generate a polished slide deck from a 3-minute spoken prompt.

  Requirements:
  • Upload or record audio
  • Output a deck as HTML presentation or PDF with ≥ 5 slides and speaker notes


```mermaid
graph TD

A[Audio Input] --> B[Voice Transcriber]
B --> C{Need Translation?}
C -->|Yes| D[Translator]
C -->|No| E[Raw Transcript]
D --> E[Raw Transcript]

E --> F[Researcher]
F --> G[Slide Outliner]

G --> H[Content Expander]
G --> I[Image Finder]

H --> J[Formatter & Stylist]
I --> J

J --> K[Speaker Notes Generator]
K --> L[Slide Renderer (HTML/PDF)]
```

---

- Audio Input – Receive an audio file or live recording as input.
- Voice Transcriber – Transcribe the spoken audio into clean, punctuated text.
- Translator – Translate the transcript into fluent English (or target language).
- Researcher – Enrich the transcript with relevant facts, examples, and context.
- Slide Outliner – Draft a structured slide outline with titles and 3–5 bullet points per slide.
- Content Expander – Expand the outline into polished, full-sentence slide content.
- Image Finder – Suggest fitting images, icons, or diagrams for each slide.
- Formatter & Stylist – Format slides with consistent tone, design style, and readability.
- Speaker Notes Generator – Write presenter notes that explain each slide in more detail.
- Slide Renderer – Assemble slides, images, and notes into an HTML or PDF presentation.
