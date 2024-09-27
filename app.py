from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from forms import CVForm
from models import db, CV
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io, os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sekretny_klucz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cv.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Katalog na zdjęcia
db.init_app(app)

@app.route("/", methods=['GET', 'POST'])
def create_cv():
    form = CVForm()
    if form.validate_on_submit():
        # Zapis danych w bazie
        photo = form.photo.data
        photo_filename = None
        if photo:
            photo_filename = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
            photo.save(photo_filename)
        
        new_cv = CV(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            experience=form.experience.data,
            education=form.education.data,
            photo_filename=photo_filename
        )
        db.session.add(new_cv)
        db.session.commit()

        flash('CV zostało zapisane', 'success')
        return redirect(url_for('list_cvs'))

    return render_template("create_cv.html", form=form)

@app.route("/cv/<int:cv_id>/pdf", methods=['GET'])
def download_cv_pdf(cv_id):
    cv = CV.query.get_or_404(cv_id)
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle(f"CV - {cv.name}")

    # Tworzenie CV w PDF
    pdf.drawString(100, 750, f"Imię i nazwisko: {cv.name}")
    pdf.drawString(100, 730, f"Adres email: {cv.email}")
    pdf.drawString(100, 710, f"Telefon: {cv.phone}")
    pdf.drawString(100, 690, f"Doświadczenie: {cv.experience}")
    pdf.drawString(100, 670, f"Wykształcenie: {cv.education}")

    # Dodanie zdjęcia do CV (jeśli istnieje)
    if cv.photo_filename:
        pdf.drawImage(cv.photo_filename, 400, 600, width=100, height=100)

    pdf.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name=f'CV_{cv.name}.pdf', mimetype='application/pdf')

@app.route("/list_cvs", methods=['GET'])
def list_cvs():
    cvs = CV.query.all()
    return render_template("list_cvs.html", cvs=cvs)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Utworzenie tabel w bazie danych, jeśli nie istnieją
    app.run(debug=True)
