import streamlit as st
import base64
import os
import requests

# Set wide mode
st.set_page_config(layout="wide")

# Card data dictionary (same as before)
cards = [
    {
        'header': 'Data Analytics Platform',
        'image': 'https://images.unsplash.com/photo-1506765515384-028b60a970df?auto=format&fit=crop&w=400&q=80',
        'description': 'A powerful platform for big data analytics and business intelligence.',
        'lob': 'Business Intelligence',
        'link': 'https://example.com/data-analytics'
    },
    {
        'header': 'Cloud Storage Service',
        'image': r'Z:/SharedDrive/images/cloud_storage.jpg',
        'description': 'Secure and scalable cloud storage solutions for enterprises.',
        'lob': 'Cloud Services',
        'link': 'https://example.com/cloud-storage'
    },
    {
        'header': 'AI-powered Chatbot',
        'image': 'https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=400&q=80',
        'description': 'Intelligent chatbot that automates customer service and support.',
        'lob': 'Artificial Intelligence',
        'link': 'https://example.com/ai-chatbot'
    },
    {
        'header': 'E-commerce Management',
        'image': r'//SharedDrive/ecommerce/ecommerce_image.png',
        'description': 'Manage all your e-commerce operations seamlessly in one place.',
        'lob': 'Retail',
        'link': 'https://example.com/ecommerce-management'
    },
    {
        'header': 'Cybersecurity Suite',
        'image': 'https://images.unsplash.com/photo-1516557070067-1aef562a6da5?auto=format&fit=crop&w=400&q=80',
        'description': 'Protect your digital assets with state-of-the-art cybersecurity tools.',
        'lob': 'Security',
        'link': 'https://example.com/cybersecurity'
    },
    {
        'header': 'Mobile Banking App',
        'image': 'https://images.unsplash.com/photo-1496307042754-b4aa456c4a2d?auto=format&fit=crop&w=400&q=80',
        'description': 'A secure and user-friendly app for all your banking needs.',
        'lob': 'Finance',
        'link': 'https://example.com/mobile-banking'
    },
]

card_style = """
<style>
    .card {
        background-color: #f9f9f9;
        border-radius: 12px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.12);
        padding: 1rem;
        display: flex;
        flex-direction: column;
        transition: box-shadow 0.3s ease;
        border: 1.5px solid transparent;
        height: 100%;
        box-sizing: border-box;
    }
    .card:hover {
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        border-color: #a3cef1;
    }
    .card img {
        width: 100%;
        height: 160px;
        object-fit: cover;
        border-radius: 10px;
        margin-bottom: 1rem;
        flex-shrink: 0;
    }
    .card-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
    }
    .card-desc {
        font-size: 0.93rem;
        color: #555;
        flex-grow: 1;
        margin-bottom: 1rem;
        line-height: 1.3;
        overflow: hidden;
        max-height: 4.5em;  /* approx 3 lines */
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 3; /* limit to 3 lines */
        -webkit-box-orient: vertical;
    }
    .card-lob {
        font-size: 0.85rem;
        font-weight: 500;
        color: #777;
        margin-bottom: 1rem;
        font-style: italic;
        flex-shrink: 0;
    }
    .card-link {
        text-align: right;
        flex-shrink: 0;
    }
    .card-link a {
        color: #1a73e8;
        font-weight: 600;
        text-decoration: none;
    }
    .card-link a:hover {
        text-decoration: underline;
    }
    /* Ensure columns stretch equally height using display flex */
    .stColumn > div {
        display: flex;
        flex-direction: column;
    }
</style>
"""

st.markdown(card_style, unsafe_allow_html=True)

search_query = st.text_input(
    "Search cards by Header, Description, or LOB Name:",
    "",
    key="search",
    placeholder="Type to search...",
)


def filter_cards(cards, query):
    if not query:
        return cards
    query_lower = query.lower()
    filtered = []
    for card in cards:
        if (
            query_lower in card["header"].lower()
            or query_lower in card["description"].lower()
            or query_lower in card["lob"].lower()
        ):
            filtered.append(card)
    return filtered


def encode_image_to_base64(image_source):
    import base64
    import requests
    from io import BytesIO
    import os

    try:
        if image_source.lower().startswith("http"):
            response = requests.get(image_source, timeout=5)
            response.raise_for_status()
            image_bytes = response.content
        else:
            with open(image_source, "rb") as f:
                image_bytes = f.read()
        encoded = base64.b64encode(image_bytes).decode()
        ext = os.path.splitext(image_source)[1].lower()
        if ext in [".jpg", ".jpeg"]:
            mime = "jpeg"
        elif ext == ".png":
            mime = "png"
        elif ext == ".gif":
            mime = "gif"
        else:
            mime = "jpeg"
        return f"data:image/{mime};base64,{encoded}"
    except Exception:
        return None


filtered_cards = filter_cards(cards, search_query)

if filtered_cards:
    num_cols = 3
    rows = (len(filtered_cards) + num_cols - 1) // num_cols

    for row in range(rows):
        cols = st.columns(num_cols, gap="large")
        for col_idx in range(num_cols):
            card_idx = row * num_cols + col_idx
            if card_idx >= len(filtered_cards):
                break
            card = filtered_cards[card_idx]
            img_data_uri = encode_image_to_base64(card["image"])
            if img_data_uri is None:
                img_html = (
                    '<div style="height:160px; background:#ccc; '
                    'border-radius:10px; margin-bottom:1rem; '
                    'display:flex; justify-content:center; align-items:center; color:#666;">'
                    "Image not found</div>"
                )
            else:
                img_html = f'<img src="{img_data_uri}" alt="{card["header"]}"/>'
            with cols[col_idx]:
                card_html = f"""
                <div class="card">
                    {img_html}
                    <div class="card-header">{card['header']}</div>
                    <div class="card-desc">{card['description']}</div>
                    <div class="card-lob">LOB: {card['lob']}</div>
                    <div class="card-link"><a href="{card['link']}" target="_blank" rel="noopener">View</a></div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
else:
    st.info("No cards found matching your search.")
