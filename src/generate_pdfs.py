from fpdf import FPDF
import os

os.makedirs("data", exist_ok=True)

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

pdf.cell(200, 10, txt="Machine Learning in Healthcare", ln=True, align='C')
pdf.ln(10)

content = """
Machine learning has revolutionized healthcare in recent years. Medical diagnosis has become 
more accurate through deep learning algorithms that can analyze medical images with precision 
comparable to expert radiologists.

Predictive analytics help hospitals forecast patient admission rates and optimize resource 
allocation. Clinical decision support systems use ML to suggest treatment options based on 
patient history and current symptoms.

Drug discovery has accelerated significantly with ML models identifying potential compounds 
faster than traditional methods. Personalized medicine uses patient genetic data to tailor 
treatments for individual needs.

Remote patient monitoring systems leverage ML to detect early warning signs of health 
deterioration. This enables proactive interventions and reduces hospital readmissions.

Challenges include data privacy concerns, algorithmic bias, and the need for regulatory 
frameworks to ensure safe deployment of AI systems in clinical settings.
"""

for line in content.strip().split('\n'):
    pdf.multi_cell(0, 10, txt=line.strip())

pdf.output("data/healthcare_ml.pdf")

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

pdf.cell(200, 10, txt="Climate Change and Renewable Energy", ln=True, align='C')
pdf.ln(10)

content = """
Climate change presents one of the most pressing challenges of our time. Rising global 
temperatures have led to melting ice caps, rising sea levels, and more frequent extreme 
weather events.

Renewable energy sources offer a sustainable alternative to fossil fuels. Solar power has 
become increasingly cost-effective with photovoltaic cell efficiency improving year over year.

Wind energy harnesses atmospheric currents to generate electricity with minimal environmental 
impact. Offshore wind farms can produce substantial amounts of clean energy.

Energy storage technology is critical for addressing the intermittent nature of renewable 
sources. Advanced battery systems and pumped hydro storage help balance supply and demand.

Government policies play a crucial role in accelerating the transition to clean energy. 
Carbon pricing mechanisms and renewable energy subsidies incentivize sustainable practices.

International cooperation is essential for meeting global climate targets. The Paris Agreement 
commits nations to limiting temperature increases and reducing greenhouse gas emissions.
"""

for line in content.strip().split('\n'):
    pdf.multi_cell(0, 10, txt=line.strip())

pdf.output("data/climate_energy.pdf")

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

pdf.cell(200, 10, txt="The Future of Quantum Computing", ln=True, align='C')
pdf.ln(10)

content = """
Quantum computing represents a paradigm shift in computational capability. Unlike classical 
computers that use bits, quantum computers leverage qubits that can exist in superposition.

Quantum algorithms like Shor's algorithm can factor large numbers exponentially faster than 
classical methods. This has significant implications for cryptography and data security.

Quantum supremacy was demonstrated when quantum computers solved problems beyond the reach 
of classical supercomputers. However, practical applications remain limited by qubit stability.

Error correction is a major challenge in quantum computing. Qubits are highly sensitive to 
environmental interference, requiring sophisticated error correction codes.

Potential applications include drug discovery, optimization problems, and materials science. 
Quantum simulations could model molecular interactions with unprecedented accuracy.

Major technology companies and research institutions are investing heavily in quantum research. 
The race is on to build stable, scalable quantum computers for practical use.
"""

for line in content.strip().split('\n'):
    pdf.multi_cell(0, 10, txt=line.strip())

pdf.output("data/quantum_computing.pdf")

print("Generated 3 PDFs in data/ folder")
