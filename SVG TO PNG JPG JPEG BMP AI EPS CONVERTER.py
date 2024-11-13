
import os
import subprocess
import cairosvg

def get_unique_filename(base_filename):
    """Generate a unique filename if the file already exists."""
    counter = 1
    base, ext = os.path.splitext(base_filename)
    new_filename = f"{base}{ext}"

    while os.path.exists(new_filename):
        new_filename = f"{base}{counter}{ext}"
        counter += 1

    return new_filename

def convert_svg(input_svg, output_file, output_format, size=None):
    """
    Convert an SVG file to various formats using CairoSVG for bmp, jpg, and jpeg,
    and Inkscape for png, eps, and ai.

    Parameters:
    - input_svg: Path to the input SVG file.
    - output_file: Path to the output file (without extension).
    - output_format: Desired output format (png, jpg, jpeg, bmp, eps, ai).
    - size: Desired size for both width and height in pixels (only for PNG).
    """
    print(f"Input SVG: {input_svg}")
    print(f"Output File: {output_file}.{output_format}")

    try:
        # Specify the full path to the Inkscape and Ghostscript executables
        inkscape_path = r"C:\Program Files\Inkscape\bin\inkscape.exe"
        gs_path = r"C:\Program Files\gs\gs10.04.0\bin\gswin64c.exe"  # Update the path to your Ghostscript executable

        # Supported formats
        supported_formats = ['png', 'jpg', 'jpeg', 'bmp', 'eps', 'ai']
        if output_format not in supported_formats:
            print(f"Unsupported format: {output_format}. Supported formats are: {', '.join(supported_formats)}")
            return

        if output_format in ['bmp', 'jpg', 'jpeg']:
            # Convert using CairoSVG
            output_filepath = get_unique_filename(output_file + '.' + output_format)
            cairosvg.svg2png(url=input_svg, write_to=output_filepath)

            print(f"{output_format.upper()} file saved as {output_filepath}")

        elif output_format == 'eps':
            # Step 1: Export as plain SVG first
            plain_svg_file = input_svg.replace('.svg', '_plain.svg')
            subprocess.run(
                [
                    inkscape_path,
                    input_svg,
                    "--export-type=svg",
                    "--export-filename=" + plain_svg_file,
                    "--export-plain-svg"
                ],
                check=True
            )

            # Step 2: Convert the plain SVG to EPS
            subprocess.run(
                [
                    inkscape_path,
                    plain_svg_file,
                    "--export-type=eps",
                    "--export-filename=" + output_file + '.' + output_format,
                    "--export-area-drawing"  # Export only the drawing area
                ],
                check=True
            )

            # Clean up the temporary plain SVG file
            if os.path.exists(plain_svg_file):
                os.remove(plain_svg_file)

        elif output_format == 'ai':
            # Step 1: Convert SVG to PDF using Inkscape
            pdf_file = output_file + '.pdf'
            subprocess.run(
                [
                    inkscape_path,
                    input_svg,
                    "--export-type=pdf",
                    "--export-filename=" + pdf_file
                ],
                check=True
            )

            # Check if the PDF file was created
            if not os.path.exists(pdf_file):
                print("Error: PDF file was not created.")
                return

            # Step 2: Prepare output filename for AI
            ai_output_file = get_unique_filename(output_file + '.ai')  # Get unique AI filename

            subprocess.run(
                [
                    gs_path,
                    "-dBATCH",
                    "-dNOPAUSE",
                    "-sDEVICE=pdfwrite",
                    "-sOutputFile=" + ai_output_file,
                    pdf_file
                ],
                check=True
            )

            # Clean up the temporary PDF file
            if os.path.exists(pdf_file):
                os.remove(pdf_file)

            print(f"AI file saved as {ai_output_file}")

        elif output_format == 'png':
            # Convert directly to PNG format using Inkscape with specified size for both dimensions
            export_command = [
                inkscape_path,
                input_svg,
                f"--export-type={output_format}",
                f"--export-filename={output_file}.{output_format}"
            ]

            # Set width and height to the same size if provided
            if size:
                export_command.append(f"--export-width={int(size)}")
                export_command.append(f"--export-height={int(size)}")

            subprocess.run(export_command, check=True)

        print(f"Conversion successful! The file has been saved as {output_file}.{output_format}")
    except subprocess.CalledProcessError as e:
        print("Error during conversion:", e)
    except FileNotFoundError:
        print("Inkscape or Ghostscript not found. Please ensure they are installed and added to your system's PATH.")
    except Exception as e:
        print("An error occurred:", e)


if __name__ == '__main__':
    # Example usage
    input_svg_file = r"C:\Users\ali.haider\Desktop\Ramadan SVG.svg"  # Replace with your SVG file path
    output_file_base = r"C:\Users\ali.haider\Downloads\Ramadan"  # Change output path base (without extension)
    desired_format = input("Enter the desired format (png, jpg, jpeg, bmp, eps, ai): ").strip().lower()

    size = None
    if desired_format == 'png':
        # Get user input for size
        size = input("Enter the desired size in pixels (both width and height will be set to this value): ")

        # Convert input to integer or None
        size = int(size) if size.strip().isdigit() else None

    convert_svg(input_svg_file, output_file_base, desired_format, size)
