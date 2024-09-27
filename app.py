from flask import Flask, render_template, request, send_file
from forms import CVForm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sekretny_klucz'

@app.route("/", methods=['GET', 'POST'])
def create_cv():
    form = CVForm()
    if form.validate_on_submit():
        # Tworzenie pliku PDF
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setTitle("CV")

        # Dane do PDF
        pdf.drawString(100, 750, f"Imię i nazwisko: {form.name.data}")
        pdf.drawString(100, 730, f"Adres email: {form.email.data}")
        pdf.drawString(100, 710, f"Telefon: {form.phone.data}")
        pdf.drawString(100, 690, f"Doświadczenie: {form.experience.data}")
        pdf.drawString(100, 670, f"Wykształcenie: {form.education.data}")

        pdf.save()
        buffer.seek(0)

        # Wysyłanie pliku PDF jako odpowiedź
        return send_file(buffer, as_attachment=True, download_name='CV.pdf', mimetype='application/pdf')

    return render_template("create_cv.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
