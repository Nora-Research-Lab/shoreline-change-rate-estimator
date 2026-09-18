import gradio as gr
import pandas as pd
from shoreline_change_rate_estimator import estimate_shoreline_change_rates
import matplotlib.pyplot as plt

def process_file(file, convention):
    try:
        df = pd.read_csv(file.name)
        
        # Validate required columns exist
        if 'date' not in df.columns or 'position_m' not in df.columns:
            raise ValueError("CSV must contain 'date' and 'position_m' columns")
        
        # Call the main function
        results = estimate_shoreline_change_rates(df, convention)
        
        # Extract results
        processed_df = results['data']
        end_point_rate = results['end_point_rate']
        regression_rate = results['regression_rate']
        r_squared = results['r_squared']
        conf_interval = results['confidence_interval']
        num_points = results['num_points']
        date_range = results['date_range']
        
        # Create plot
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(processed_df['decimal_year'], processed_df['position_m'], label='Data Points', color='blue')
        ax.plot(processed_df['decimal_year'], processed_df['fitted_values'], label='Regression Line', color='red')
        ax.set_xlabel('Decimal Year')
        ax.set_ylabel('Position (m)')
        ax.set_title('Shoreline Position vs Time')
        ax.legend()
        ax.grid(True)
        
        # Format summary text
        summary_text = f"""
End-Point Rate: {end_point_rate:.4f} m/year
Linear Regression Rate: {regression_rate:.4f} m/year
R²: {r_squared:.4f}
95% Confidence Interval: [{conf_interval[0]:.4f}, {conf_interval[1]:.4f}] m/year
Number of Data Points: {num_points}
Date Range: {date_range[0]} to {date_range[1]}
        """.strip()
        
        return processed_df[['date', 'position_m', 'decimal_year']], fig, summary_text
        
    except Exception as e:
        # Return empty results with error message
        return pd.DataFrame(), plt.figure(), f"Error processing file: {str(e)}"

with gr.Blocks() as demo:
    gr.Markdown("# Shoreline Change Rate Estimator")
    
    with gr.Row():
        with gr.Column():
            file_input = gr.File(label="Upload CSV File", file_types=[".csv"])
            convention_radio = gr.Radio(
                choices=["seaward_positive", "landward_positive"],
                value="seaward_positive",
                label="Convention"
            )
            submit_btn = gr.Button("Calculate Rates")
        
        with gr.Column():
            data_table = gr.Dataframe(label="Parsed Data")
            plot_output = gr.Plot(label="Position vs Time Plot")
            summary_output = gr.Textbox(label="Results Summary", lines=8)

    submit_btn.click(
        fn=process_file,
        inputs=[file_input, convention_radio],
        outputs=[data_table, plot_output, summary_output]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
