import streamlit as st
import requests


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="LegalEase AI",
    page_icon="⚖️",
    layout="centered"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("⚖️ LegalEase AI")

st.subheader(
    "AI-Powered Legal Document Generator"
)

st.write(
    "Create professional legal document templates "
    "using Generative AI."
)


# --------------------------------------------------
# DOCUMENT TYPE
# --------------------------------------------------

document_type = st.selectbox(
    "Select Document Type",
    [
        "Employment Contract",
        "Lease Agreement",
        "Non-Disclosure Agreement",
        "Service Agreement",
        "Freelance Agreement",
        "Partnership Agreement",
        "Offer Letter"
    ]
)


# --------------------------------------------------
# PARTIES
# --------------------------------------------------

parties = st.text_area(
    "Parties Involved",
    placeholder=(
        "Example:\n"
        "ABC Technologies Pvt Ltd\n"
        "John Doe"
    ),
    height=120
)


# --------------------------------------------------
# TERMS
# --------------------------------------------------

terms = st.text_area(
    "Key Terms & Conditions",
    placeholder=(
        "Example:\n"
        "Salary is ₹25,000 per month;\n"
        "Contract duration is one year;\n"
        "Either party can terminate with 30 days notice."
    ),
    height=180
)


# --------------------------------------------------
# EFFECTIVE DATE
# --------------------------------------------------

effective_date = st.date_input(
    "Effective Date"
)


# --------------------------------------------------
# GENERATE BUTTON
# --------------------------------------------------

if st.button(
    "Generate Document",
    key="generate_document",
    use_container_width=True
):

    # Check required fields

    if not parties.strip():

        st.warning(
            "Please enter the parties involved."
        )

    elif not terms.strip():

        st.warning(
            "Please enter the key terms and conditions."
        )

    else:

        data = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "effective_date": str(effective_date)
        }

        try:

            with st.spinner(
                "Generating your legal document..."
            ):

                response = requests.post(
                    "http://127.0.0.1:8000/api/generate",
                    json=data,
                    timeout=120
                )


            # --------------------------------------------------
            # SUCCESS
            # --------------------------------------------------

            if response.status_code == 200:

                result = response.json()

                st.success(
                    "Document generated successfully!"
                )

                generated_document = result.get(
                    "document",
                    ""
                )

                st.subheader(
                    "Generated Legal Document"
                )

                edited_document = st.text_area(
                    "Review and Edit",
                    value=generated_document,
                    height=600,
                    key="generated_document_editor"
                )

                # Download TXT

                st.download_button(
                    "📄 Download TXT",
                    data=edited_document,
                    file_name="legal_document.txt",
                    mime="text/plain",
                    key="download_txt"
                )


            # --------------------------------------------------
            # BACKEND ERROR
            # --------------------------------------------------

            else:

                st.error(
                    f"Backend returned error "
                    f"{response.status_code}"
                )

                st.code(
                    response.text
                )


        # --------------------------------------------------
        # CONNECTION ERROR
        # --------------------------------------------------

        except requests.exceptions.ConnectionError:

            st.error(
                """
Cannot connect to the FastAPI backend.

Make sure this is running in another terminal:

python -m uvicorn backend.main:app --reload
"""
            )


        # --------------------------------------------------
        # TIMEOUT
        # --------------------------------------------------

        except requests.exceptions.Timeout:

            st.error(
                "The request took too long. "
                "Please try again."
            )


        # --------------------------------------------------
        # OTHER ERROR
        # --------------------------------------------------

        except Exception as e:

            st.error(
                f"Unexpected error: {str(e)}"
            )


# --------------------------------------------------
# DISCLAIMER
# --------------------------------------------------

st.divider()

st.caption(
    "⚠️ LegalEase generates AI-assisted document templates. "
    "Review important legal documents with a qualified "
    "legal professional before use."
)