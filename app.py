import gradio as gr
import numpy as np

# Simple beam deflection calculation
def beam_deflection(L, load_type, load_value, E, I):
    """
    Calculate deflection along a simply supported beam.
    Returns positions and deflection as a string for safe display.
    """
    L = float(L)
    load_value = float(load_value)
    E = float(E)
    I = float(I)

    x = np.linspace(0, L, 50)  # 50 points along the beam

    # Calculate deflection using simple formulas
    if load_type == "point":
        # Maximum deflection at center: δ = (P*L^3)/(48*E*I)
        delta_max = (load_value * L**3) / (48 * E * I)
        y = 4*delta_max/(L**2) * x * (L-x)  # parabolic distribution
    else:  # UDL
        # Maximum deflection: δ = (5*w*L^4)/(384*E*I)
        delta_max = (5 * load_value * L**4) / (384 * E * I)
        y = (delta_max * 16 / L**4) * (x**2) * (L - x)**2

    # Convert to simple string for display
    display_str = "x(m)   deflection(m)\n"
    for xi, yi in zip(x, y):
        display_str += f"{xi:.2f}   {yi:.6e}\n"

    return f"Maximum Deflection: {delta_max:.6e} m", display_str

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## Beam Deflection Calculator (Safe Version, No Errors)")
    
    with gr.Row():
        with gr.Column(scale=1):
            L = gr.Number(value=1.0, label="Beam Length L (m)")
            load_type = gr.Radio(["point", "udl"], value="point", label="Load Type")
            load_value = gr.Number(value=100.0, label="Load: P (N) for point / w (N/m) for UDL")
            E = gr.Number(value=2.1e11, label="Young's Modulus E (Pa)")
            I = gr.Number(value=1e-6, label="Moment of Inertia I (m^4)")
            run_btn = gr.Button("Compute Deflection")
        
        with gr.Column(scale=2):
            output_text = gr.Textbox(label="Maximum Deflection")
            output_curve = gr.Textbox(label="Deflection Curve (x vs y)")

    run_btn.click(
        fn=beam_deflection,
        inputs=[L, load_type, load_value, E, I],
        outputs=[output_text, output_curve]
    )

demo.launch()

