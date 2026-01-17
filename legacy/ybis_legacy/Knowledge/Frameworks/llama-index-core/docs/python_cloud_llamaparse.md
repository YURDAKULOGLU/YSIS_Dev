 Overview of LlamaParse | LlamaIndex Python Documentation
  [Skip to content](#_top)

# Overview of LlamaParse

**Transform unstructured documents into LLM-ready data**

Built for teams that care about quality, LlamaParse turns complex, messy files into structured, clean outputs.

LlamaParse is a highly accurate parser for complex documents like financial reports, research papers, and scanned PDFs. It handles tables, images, and charts with ease—so you can skip the cleanup and get straight to using your data

![parse document comparison](/python/_astro/parse_comparison.h1v__IZo_2beC10.webp)

  
  

## Core Features

[Section titled “Core Features”](#core-features)

* **Flexible Parsing** - Choose between *Cost Effective*, *Agentic*, *Agentic Plus* and *Use-case Oriented* [presets](/python/cloud/llamaparse/presets_and_modes/presets) to handle everything from simple text to visually complex documents. For more advanced parsing, the [Advanced Settings](/python/cloud/llamaparse/presets_and_modes/advance_parsing_modes) allows you to pick-and-choose what works for you.
* **Broad File Support** - Parse PDFs, DOCX, PPTX, XLSX, HTML, JPEG, XML, EPUB, and [many more →](/python/cloud/llamaparse/features/supported_document_types/).
* **Multimodal & Custom Output** - Accurately extract tables, charts, images, and diagrams into structured formats. Use custom prompt instructions to tailor the output the way you want it.

  
  

## Workflow

[Section titled “Workflow”](#workflow)

1. **Connect your documents**  
   Upload or stream documents via our API, Clients, or UI—with built-in connectors to sync with enterprise data sources.
2. **Configure your parsing**  
   Select a preset for a quick start, or define a custom configuration with specific models, output formats, and parsing instructions tailored to your use case.
3. **Get clean, structured results**  
   Receive parsed output in text, markdown, or JSON—ready to plug into your application, database, or LLM pipeline.

  
  

## Why LlamaParse?

[Section titled “Why LlamaParse?”](#why-llamaparse)

High-quality document parsing is one of the most overlooked—yet crucial—steps in the LLM stack. Models can only reason with the information you give them, and most documents today are hard for LLMs to interpret out of the box.

LlamaParse was built to solve this problem from the ground up. Unlike generic OCR or PDF-to-text tools, LlamaParse uses AI-native methods to understand structure, layout, and intent—ensuring every output is optimized for downstream LLM consumption.