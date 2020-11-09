import base64
from PIL import Image
import os

# Wraps images in HTML and inserts them one after the other
def figures_to_paragraph(fig_names, fig_dir):
    figures_html=""
    current_dir = os.getcwd()
    os.chdir(fig_dir)
    for fig in fig_names:
        im=open(fig, 'rb')
        encoded = base64.b64encode(im.read()).decode('utf-8')
        figures_html+=(f'<p><img src="data:image/png;base64,{encoded}"></p>')
    os.chdir(current_dir)
    return figures_html

# HTML report structure
def weekly_report_wrapper(table, fig_names, fig_dir):
    figures_as_html=figures_to_paragraph(fig_names, fig_dir)

    wrapper =(
        "<html>"+
    
    
        "<head>"+
        "<title>Weekly report</title>"+
        "</head>"+
    
        "<body>" +
        figures_as_html +
        f"<p>{table}</p>" +
        "</body>" +
    
    
        "</html>"
    )
    return wrapper

