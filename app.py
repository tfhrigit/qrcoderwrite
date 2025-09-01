from flask import Flask, render_template, request, send_file, redirect, url_for
import qrcode
from io import BytesIO
from base64 import b64encode
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_code = None
    if request.method == 'POST':
        data = request.form.get('data')
        if data:
            # Generate QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            # Create QR code image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save image to bytes buffer
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            
            # Encode image for display
            encoded_image = b64encode(buffer.getvalue()).decode('utf-8')
            qr_code = f"data:image/png;base64,{encoded_image}"
            
            # Store the image in session for download
            from flask import session
            session['qr_code'] = buffer.getvalue()
            
    return render_template('index.html', qr_code=qr_code)

@app.route('/download')
def download():
    from flask import session
    qr_code = session.get('qr_code')
    if qr_code:
        buffer = BytesIO(qr_code)
        buffer.seek(0)
        return send_file(buffer, mimetype='image/png', as_attachment=True, download_name='qrcode.png')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'your_secret_key_here'  # Ganti dengan secret key yang aman
    app.run(debug=True)