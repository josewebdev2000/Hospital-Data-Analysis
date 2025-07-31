import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os
from IPython.display import Image as IPImage, display, clear_output
import uuid

# Ensure required libraries are installed
try:
    import matplotlib
    import numpy
    import pandas
    from PIL import Image
except ImportError as e:
    print(f"Missing library: {e}. Install with: pip install matplotlib numpy pandas pillow")
    raise

# Clear previous output to avoid duplicates
clear_output(wait=True)

# Hospital data as a DataFrame
data = {
    "Hospital Name": [
        "Broward Health Coral Springs", "Broward Health Imperial Point", "Broward Health Medical Center",
        "Broward Health North", "Cleveland Clinic Florida - Weston", "Encompass Health Rehabilitation Hospital",
        "Fort Lauderdale Behavioral Health Center", "HCA Florida Northwest Hospital", "HCA Florida University Hospital",
        "HCA Florida Westside Hospital", "HCA Florida Woodmont Hospital", "Holy Cross Health",
        "Kindred Hospital South Florida Ft Lauderdale", "Larkin Community Hospital Behavioral Health",
        "Memorial Hospital Miramar", "Memorial Hospital Pembroke", "Memorial Hospital West",
        "Memorial Regional Hospital", "St Anthonys Rehabilitation Hospital"
    ],
    "Debt to Equity Ratio": [0.07, 0.24, 0.16, 0.08, 0.01, 0.0, 0.67, -0.63, -37.22, -0.88, -0.88, 1.27, -0.98, 0.42, 0.01, 0.07, 0.01, 1.48, -0.27],
    "Days Cash on Hand": [0.0, 0.0, 60.1, 0.0, 55.7, 67.6, -2.7, 0.0, 0.0, 0.0, -0.3, 16.7, -0.5, 19.1, 0.6, 1.4, 0.4, 325.9, 28.7],
    "Days Sales Outstanding": [42.3, 40.1, 60.1, 47.7, 55.7, 53.8, 33.9, 3.7, 52.8, 3.6, 0.0, 51.8, 107.3, 28.8, 27.7, 30.2, 39.1, 51.4, 34.2],
    "Bad Debt to Accounts Receivable Ratio": [0.386, 0.357, 0.398, 0.376, 0.153, 0.0, 0.0, 0.402, 0.103, 0.317, 0.713, 0.241, 0.0, 0.0, 0.077, 0.101, 0.037, 0.034, 0.0],
    "Labor Compensation Ratio": [0.432, 0.498, 0.462, 0.459, 0.283, 0.51, 0.061, 0.281, 0.359, 0.272, 0.326, 0.477, 0.063, 0.056, 0.381, 0.474, 0.4, 1.11, 0.084],
    "Asset Turnover": [0.685253, 1.12811, 0.603911, 0.993378, 1.3777, 1.00866, 0.639097, 1.66223, 0.431683, 2.42841, 2.83326, 1.33701, 2.03363, 0.81484, 2.55485, 3.69155, 1.77093, 0.455503, 2.44677]
}
df = pd.DataFrame(data)

# Chart configurations
charts = [
    {
        "title": "Debt to Equity Ratio (Top 5 Hospitals)",
        "description": "Debt to Equity Ratio measures debt relative to equity, with lower ratios indicating financial stability. This chart shows the top 5 hospitals with the lowest ratios.\nConclusion: Cleveland Clinic Florida - Weston and Memorial hospitals show strong stability with ratios of 0.01.",
        "type": "bar",
        "data": df.sort_values("Debt to Equity Ratio").head(5)[["Hospital Name", "Debt to Equity Ratio"]],
        "x": "Hospital Name",
        "y": "Debt to Equity Ratio",
        "color": "#3B82F6",
        "xlabel": "Hospital",
        "ylabel": "Debt to Equity Ratio"
    },
    {
        "title": "Days Cash on Hand (Top 5 Hospitals)",
        "description": "Days Cash on Hand shows how long a hospital can operate without revenue, reflecting liquidity. This chart displays the top 5 hospitals.\nConclusion: Memorial Regional Hospital’s 325.9 days indicate exceptional liquidity.",
        "type": "line",
        "data": df.sort_values("Days Cash on Hand", ascending=False).head(5)[["Hospital Name", "Days Cash on Hand"]],
        "x": "Hospital Name",
        "y": "Days Cash on Hand",
        "color": "#10B981",
        "xlabel": "Hospital",
        "ylabel": "Days Cash on Hand"
    },
    {
        "title": "Bad Debt to Accounts Receivable Ratio (Top 5 Hospitals)",
        "description": "This ratio measures uncollectible receivables, with lower values showing better management. This chart highlights the top 5 hospitals.\nConclusion: Memorial Hospital West’s 3.7% ratio reflects efficient receivables management.",
        "type": "pie",
        "data": df[df["Bad Debt to Accounts Receivable Ratio"] > 0].sort_values("Bad Debt to Accounts Receivable Ratio").head(5)[["Hospital Name", "Bad Debt to Accounts Receivable Ratio"]],
        "labels": "Hospital Name",
        "values": "Bad Debt to Accounts Receivable Ratio",
        "colors": ["#3B82F6", "#10B981", "#8B5CF6", "#F59E0B", "#EF4444"]
    },
    {
        "title": "Days Sales Outstanding vs. Asset Turnover (All Hospitals)",
        "description": "Days Sales Outstanding (DSO) measures collection speed; Asset Turnover shows asset efficiency. This chart plots both for all hospitals.\nConclusion: HCA Florida Westside’s low DSO (3.6 days) and high Asset Turnover (2.43) indicate efficient operations.",
        "type": "scatter",
        "data": df[["Hospital Name", "Days Sales Outstanding", "Asset Turnover"]],
        "x": "Days Sales Outstanding",
        "y": "Asset Turnover",
        "color": "#F59E0B",
        "xlabel": "Days Sales Outstanding",
        "ylabel": "Asset Turnover"
    },
    {
        "title": "Financial Metrics Comparison (Top 5 by Days Cash on Hand)",
        "description": "This chart compares Debt to Equity, Days Cash on Hand, and Labor Compensation Ratio for the top 5 hospitals by liquidity.\nConclusion: Encompass Health’s zero Debt to Equity Ratio balances its high labor costs.",
        "type": "radar",
        "data": df.sort_values("Days Cash on Hand", ascending=False).head(5)[["Hospital Name", "Debt to Equity Ratio", "Days Cash on Hand", "Labor Compensation Ratio"]],
        "labels": ["Debt to Equity Ratio", "Days Cash on Hand", "Labor Compensation Ratio"],
        "colors": ["#3B82F6", "#10B981", "#8B5CF6", "#F59E0B", "#EF4444"]
    },
    {
        "title": "Labor Compensation Ratio (Top 5 by Asset Turnover)",
        "description": "Labor Compensation Ratio measures labor costs relative to revenue, with lower ratios indicating efficiency. This chart shows the top 5 by Asset Turnover.\nConclusion: St Anthonys’ 8.4% ratio reflects high labor cost efficiency.",
        "type": "area",
        "data": df.sort_values("Asset Turnover", ascending=False).head(5)[["Hospital Name", "Labor Compensation Ratio"]],
        "x": "Hospital Name",
        "y": "Labor Compensation Ratio",
        "color": "#EF4444",
        "xlabel": "Hospital",
        "ylabel": "Labor Compensation Ratio"
    }
]

# Function to wrap text for PIL
def wrap_text(text, font, max_width):
    lines = []
    for paragraph in text.split('\n'):
        words = paragraph.split()
        current_line = []
        current_width = 0
        for word in words:
            word_width = font.getbbox(word + ' ')[2]
            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width
        if current_line:
            lines.append(' '.join(current_line))
        lines.append('')  # Add empty line for paragraph break
    return [line for line in lines if line]

# Create and save charts
output_files = []
for idx, chart in enumerate(charts):
    # Create figure for chart (1000x750 pixels, ~10x7.5 inches at 100 DPI)
    fig = plt.figure(figsize=(10, 7.5), dpi=100)
    
    try:
        if chart["type"] == "bar":
            plt.bar(chart["data"][chart["x"]], chart["data"][chart["y"]], color=chart["color"], edgecolor="#1E40AF")
            plt.xlabel(chart["xlabel"], fontsize=14)
            plt.ylabel(chart["ylabel"], fontsize=14)
            plt.xticks(rotation=45, ha='right', fontsize=12)
            plt.yticks(fontsize=12)
            plt.tight_layout()
        
        elif chart["type"] == "line":
            plt.plot(chart["data"][chart["x"]], chart["data"][chart["y"]], color=chart["color"], marker='o')
            plt.xlabel(chart["xlabel"], fontsize=14)
            plt.ylabel(chart["ylabel"], fontsize=14)
            plt.xticks(rotation=45, ha='right', fontsize=12)
            plt.yticks(fontsize=12)
            plt.tight_layout()
        
        elif chart["type"] == "pie":
            plt.pie(chart["data"][chart["values"]], labels=chart["data"][chart["labels"]], 
                    colors=chart["colors"], autopct='%1.1f%%', textprops={'fontsize': 10})
            plt.axis('equal')
        
        elif chart["type"] == "scatter":
            plt.scatter(chart["data"][chart["x"]], chart["data"][chart["y"]], color=chart["color"], s=50)
            plt.xlabel(chart["xlabel"], fontsize=14)
            plt.ylabel(chart["ylabel"], fontsize=14)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            plt.tight_layout()
        
        elif chart["type"] == "radar":
            labels = chart["labels"]
            num_vars = len(labels)
            angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
            angles += angles[:1]
            print(f"Chart 5: Processing {len(chart['data'])} hospitals with labels: {labels}")
            for i, row in chart["data"].iterrows():
                # Normalize data to [0, 1] range for radar chart
                values = row[labels].copy()
                max_values = [2.0, 350.0, 1.2]  # Fixed max values for Debt to Equity, Days Cash, Labor Comp
                values = [v / max_v if max_v != 0 else v for v, max_v in zip(values, max_values)]
                values += values[:1]
                color = chart["colors"][i % len(chart["colors"])]  # Safe color access
                plt.polar(angles, values, label=row["Hospital Name"], color=color)
                plt.fill(angles, values, alpha=0.25, color=color)
            plt.xticks(angles[:-1], labels, fontsize=12)
            plt.legend(loc='center left', bbox_to_anchor=(1.1, 0.5), fontsize=10)
        
        elif chart["type"] == "area":
            plt.fill_between(chart["data"][chart["x"]], chart["data"][chart["y"]], color=chart["color"], alpha=0.6)
            plt.xlabel(chart["xlabel"], fontsize=14)
            plt.ylabel(chart["ylabel"], fontsize=14)
            plt.xticks(rotation=45, ha='right', fontsize=12)
            plt.yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5], [f"{x*100:.0f}%" for x in [0, 0.1, 0.2, 0.3, 0.4, 0.5]], fontsize=12)
            plt.tight_layout()
        
        # Save chart to temporary file
        temp_filename = f"temp_chart_{uuid.uuid4()}.png"
        plt.savefig(temp_filename, bbox_inches='tight', dpi=100)
        plt.close()
        
        # Create final image with title and description
        final_image = Image.new('RGB', (1000, 900), 'white')
        draw = ImageDraw.Draw(final_image)
        
        # Load fonts with multiple fallbacks
        try:
            title_font = ImageFont.truetype("arialbd.ttf", 20) if os.path.exists("arialbd.ttf") else \
                         ImageFont.truetype("DejaVuSans-Bold.ttf", 20) if os.path.exists("DejaVuSans-Bold.ttf") else \
                         ImageFont.truetype("LiberationSans-Bold.ttf", 20) if os.path.exists("LiberationSans-Bold.ttf") else \
                         ImageFont.truetype("Helvetica-Bold.ttf", 20) if os.path.exists("Helvetica-Bold.ttf") else \
                         ImageFont.load_default()
            text_font = ImageFont.truetype("arial.ttf", 16) if os.path.exists("arial.ttf") else \
                        ImageFont.truetype("DejaVuSans.ttf", 16) if os.path.exists("DejaVuSans.ttf") else \
                        ImageFont.truetype("LiberationSans-Regular.ttf", 16) if os.path.exists("LiberationSans-Regular.ttf") else \
                        ImageFont.truetype("Helvetica.ttf", 16) if os.path.exists("Helvetica.ttf") else \
                        ImageFont.load_default()
        except Exception as e:
            print(f"Font loading failed: {e}. Using default PIL font.")
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
        
        # Draw title
        draw.text((20, 20), chart["title"], fill="#1E40AF", font=title_font)
        
        # Draw wrapped description
        wrapped_text = wrap_text(chart["description"], text_font, 960)
        y_text = 60
        for line in wrapped_text:
            draw.text((20, y_text), line, fill="black", font=text_font)
            y_text += 25
        
        # Paste chart image
        chart_image = Image.open(temp_filename)
        chart_image = chart_image.resize((1000, 750), Image.Resampling.LANCZOS)
        final_image.paste(chart_image, (0, 150))
        
        # Save final image
        output_filename = f"chart_{idx+1}_{chart['title'].replace(' ', '_').lower()}.png"
        final_image.save(output_filename)
        output_files.append(output_filename)
        
        # Clean up temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
    
    except Exception as e:
        print(f"Error generating chart {idx+1} ({chart['title']}): {e}")
        plt.close()
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        continue

# Display output files once
print("Charts saved as PNG files in the current directory:")
for file in output_files:
    print(file)
    display(IPImage(file))