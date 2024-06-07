import qrcode
from PIL import Image
import streamlit as st

filename = "qr_codes/qr_code.png"
    
def generate_qr_code_with_logo(url, filename, logo_path=""):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Use high error correction level
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    if logo_path:
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

        # Add logo in the center
        logo = Image.open(logo_path)

        # Ensure logo has an alpha channel
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')

        # Calculate dimensions
        logo_size = 70
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

        # Create a transparent layer the size of the QR code
        qr_size = img.size[0]
        qr_with_logo = Image.new("RGBA", (qr_size, qr_size))
        qr_with_logo.paste(img, (0, 0))

        # Position the logo at the center
        pos = ((qr_size - logo_size) // 2, (qr_size - logo_size) // 2)
        qr_with_logo.paste(logo, pos, logo)

        # Save the final image
        qr_with_logo = qr_with_logo.convert('RGB')  # Remove alpha for saving in JPEG format
        qr_with_logo.save(filename)
    else:
        img.save(filename)

# Create a Streamlit app 
st.set_page_config(page_title="QR Code Generator", page_icon="🌐", layout="centered")
st.image("images/supports.JPG", use_column_width=True)
st.title("QR Code Generator")
url = st.text_input("Enter the URL")
logo_path = st.file_uploader("Upload a logo for the QR code (optional)")

if st.button("Generate QR Code"):
    if logo_path is not None:
        generate_qr_code_with_logo(url, filename, logo_path)
    else:
        generate_qr_code(url, filename)
        
    st.image(filename, use_column_width=True)
    with open(filename, "rb") as f:
        image_data = f.read()  
    download = st.download_button(label="Download QR", data=image_data, file_name="qr_generated.png")
