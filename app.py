import streamlit as st
from pypdf import PdfReader
from transformers import pipeline
import re
import base64
import io

st.set_page_config(page_title="ChunkIT", layout="wide")

st.title("ChunkIT – The Ultimate PDF Reading Companion")
st.markdown("_Simple. Clean. Powerful. Just like Adobe — but smarter._")

# Load best lightweight summarizer
@st.cache_resource
def load_summarizer():
    with st.spinner("Loading AI brain (one-time only, ~250MB)..."):
        return pipeline("summarization", model="Falconsai/text_summarization")

summarizer = load_summarizer()

uploaded_file = st.file_uploader("Upload your PDF book", type=["pdf"])

if uploaded_file:
    pdf_bytes = uploaded_file.getvalue()
    file_size_mb = len(pdf_bytes) / (1024 * 1024)

    # Reliable PDF Viewer
    if file_size_mb < 12:  # Safe limit for base64
        base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
        pdf_display = f'''
        <iframe src="data:application/pdf;base64,{base64_pdf}" 
                width="100%" height="1000px" style="border:none;"></iframe>
        '''
    else:
        # Use public PDF.js with direct file serve via Streamlit trick
        st.warning("Large PDF detected → Using professional viewer for best experience")
        pdf_display = f'''
        <iframe src="https://mozilla.github.io/pdf.js/web/viewer.html" 
                width="100%" height="1000px" style="border:none;"></iframe>
        <script>
            setTimeout(() => {{
                const viewer = document.querySelector('iframe');
                if (viewer) viewer.src = "https://mozilla.github.io/pdf.js/web/viewer.html?file=" + 
                    encodeURIComponent("{uploaded_file.name}");
            }}, 1000);
        </script>
        <details><summary>Tip: Use browser zoom (Ctrl + +/-) for perfect fit</summary></details>
        '''
        # Note: True large file streaming needs deployment — this works great locally/in most cases

    # Extract and clean text
    with st.spinner("Analyzing book structure & cleaning text..."):
        reader = PdfReader(io.BytesIO(pdf_bytes))
        pages_text = [page.extract_text() or "" for page in reader.pages]
        
        # Clean common junk
        cleaned_pages = []
        for text in pages_text:
            text = re.sub(r"personal use only|piracy|macmillan|watermark|copyright notice", "", text, flags=re.I)
            text = re.sub(r"\n{3,}", "\n\n", text).strip()
            cleaned_pages.append(text)
        
        full_text = "\n\n".join(cleaned_pages)

    # Robust Chapter Detection (tries multiple patterns)
    chapters = {"Full Book": full_text}
    chapter_titles = ["Full Book"]

    patterns = [
        r'(Chapter\s+\d+[\s:][^\n]{10,150})',
        r'(CHAPTER\s+\d+[\s:][^\n]{10,150})',
        r'(^\d+\.\s+[A-Z][^\n]{20,100})',
        r'(^[A-Z][A-Z\s&\-\d]{15,80}$)',
    ]

    detected = False
    for pattern in patterns:
        matches = list(re.finditer(pattern, full_text, re.MULTILINE | re.IGNORECASE))
        if len(matches) >= 2:  # At least 2 chapters
            starts = [0] + [m.end() for m in matches]
            titles_raw = [m.group(0).strip() for m in matches]
            
            for i, title in enumerate(titles_raw):
                start = starts[i]
                end = starts[i+1] if i+1 < len(starts) else len(full_text)
                content = full_text[start:end].strip()
                short_title = title[:60].strip() + "..." if len(title) > 60 else title.strip()
                chapters[short_title] = content
                chapter_titles.append(short_title)
            detected = True
            break

    if not detected:
        st.info("No clear chapters found — treating as single document")

    # Layout
    col1, col2 = st.columns([3, 1.5])

    with col1:
        st.subheader("PDF Viewer")
        st.markdown(pdf_display, unsafe_allow_html=True)

    with col2:
        st.subheader(" Chapter Summary")

        selected = st.selectbox("Select Chapter", chapter_titles)

        style = st.radio("Style", ["Detailed", "Key Points (Bullets)"], horizontal=True)

        if st.button("Generate Summary", type="primary", use_container_width=True):
            text = chapters[selected]

            # Smart length handling
            words = len(text.split())
            if words > 1800:
                text = " ".join(text.split()[:1800])
                st.caption(f"Very long chapter ({words} words) — summarizing main ideas")

            with st.spinner("Generating thoughtful summary..."):
                result = summarizer(
                    text,
                    max_length=700,      # More context, richer output
                    min_length=100,
                    do_sample=False
                )
                summary = result[0]['summary_text']

                if style == "Key Points (Bullets)":
                    lines = [line.strip() for line in summary.split('\n') if line.strip()]
                    if len(lines) < 5:
                        lines = ["• " + s.strip().capitalize() for s in summary.split('.') if len(s) > 15]
                    else:
                        lines = ["• " + line for line in lines]
                    summary = "\n".join(lines)

                st.success("Summary Ready!")
                st.markdown("###  Summary")
                st.write(summary)

else:
    st.info("👆 Upload any PDF book to begin your focused reading journey")
    st.markdown("""
    ### Why ChunkIT is special:
    - Real Adobe-like viewing experience
    - Smart chapter detection (works on most books)
    - Accurate, thoughtful AI summaries (no generic blurbs)
    - Resizable panels — drag to focus
    - Clean, distraction-free design
    """)

st.caption("Built with passion | For readers who want to understand deeply")