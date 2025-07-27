Intelligent Document Analysis System

This project implements a lightweight, context-aware PDF document analysis tool. It is designed to extract and prioritize the most relevant sections of text from a collection of PDFs, based on a provided persona and job-to-be-done (JTBD).

* A set of PDF documents (e.g., travel guides, manuals, reports)
* A target persona (e.g., a first-time visitor to France)
* A job-to-be-done (e.g., wants to explore authentic local cuisine)

Goal:
* Identify and return the most contextually relevant and meaningful sections from the PDFs to help users find exactly what they care about.
 
Approach:

1. Text Extraction**

   * Extracts page-wise text from each PDF using **PyMuPDF**.

2. Section Segmentation

   * Splits text into logical sections using formatting cues like headings and page breaks.

3. Relevance Ranking

   * Uses **TF-IDF vectorization** and **cosine similarity** to score sections against the persona and JTBD.

4. Subsection Refinement

   * Further filters top sections using keyword matching and sentence importance.

5. Structured Output

   * Stores final ranked sections and insights in `output/output.json` with page numbers and titles.

---

Libraries and Tools Used

* PyMuPDF: For PDF reading and page-level text extraction
* scikit-learn: For TF-IDF and cosine similarity
* NLTK: For tokenization and basic text processing
* json, os: For configuration and file I/O
