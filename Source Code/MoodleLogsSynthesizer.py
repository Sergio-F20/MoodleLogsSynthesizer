import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from tkinter import Tk, filedialog

import subprocess
import sys
import pandas as pd

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter

def create_shortened_alfa_report():
    try:
        def get_file_paths():
            root = Tk()
            root.withdraw()

            # Prompt the user to select the CSV files
            csv_paths = filedialog.askopenfilenames(
                title='Select CSV Files', filetypes=[('CSV Files', '*.csv')])

            # Prompt the user to select the output PDF file path
            pdf_path = filedialog.asksaveasfilename(
                title='Save PDF File', defaultextension='.pdf', filetypes=[('PDF Files', '*.pdf')])

            return csv_paths, pdf_path

        def process_csv_files(csv_paths):
            try:
                dfs = []
                oldest_time = None
                newest_time = None

                for path in csv_paths:
                    df = pd.read_csv(path)

                    # Retrieve the oldest and newest time
                    time_col = df['Time']
                    if oldest_time is None or time_col.min() < oldest_time:
                        oldest_time = time_col.min()
                    if newest_time is None or time_col.max() > newest_time:
                        newest_time = time_col.max()

                    dfs.append(df)

                # Format the oldest and newest time as strings
                oldest_time_str = str(oldest_time)
                newest_time_str = str(newest_time)

                # Concatenate the DataFrames into a single DataFrame
                if len(dfs) > 0:
                    df = pd.concat(dfs)

                    # Perform the pivot table operation
                    pivot_table = df.pivot_table(
                        index='User full name', aggfunc='size', fill_value=0)

                    return pivot_table, oldest_time_str, newest_time_str
                else:
                    messagebox.showwarning("Warning", "No CSV files selected!")
                    return None, None, None
            except Exception as e:
                messagebox.showerror(
                    "Error", f"An error occurred while processing CSV files: {str(e)}")

        def generate_pdf(pivot_table, pdf_path, oldest_time_str, newest_time_str):
            try:
                # Create a new PDF document
                c = canvas.Canvas(pdf_path)

                # Set up the table layout
                row_height = 20
                column_width = 300
                margin = 50
                max_rows_per_page = 30  # Maximum number of rows per page

                # Write the time range as text in the PDF
                c.setFont("Helvetica-Bold", 13)
                c.drawString(
                    margin, 819, f"Attendance Report. From {oldest_time_str} to {newest_time_str}")

                # Sort the pivot table by the total count of event names
                pivot_table = pivot_table.sort_index()

                # Write the table headers
                c.setFont("Helvetica-Bold", 12)
                c.drawString(margin, 800, "User full name")
                c.drawString(margin + column_width, 800, "Count of Event name")

                # Draw a horizontal line below the column headers
                c.setStrokeColor(colors.darkblue)
                c.setLineWidth(1)
                c.line(margin, 795, margin + 2 * column_width, 795)

                # Write the table content
                c.setFont("Helvetica", 12)
                x = margin
                y = 780  # Adjust the initial y-coordinate to leave space for headers
                rows_written = 0
                for user, count in pivot_table.items():

                    # Check if the content exceeds the page height
                    if y < margin:
                        # Create a new page
                        c.showPage()
                        # Reset the y-coordinate
                        y = 780
                        # Write the table headers
                        c.setFont("Helvetica-Bold", 12)
                        c.drawString(margin, 800, "User full name")
                        c.drawString(margin + column_width,
                                     800, "Count of Event name")
                        # Draw a horizontal line below the column headers
                        c.setStrokeColor(colors.darkblue)
                        c.setLineWidth(1)
                        c.line(margin, 795, margin + 2 * column_width, 795)
                        # Write the table content
                        c.setFont("Helvetica", 12)

                    # Set the font to regular and black color for user name and count
                    c.setFillColor(colors.black)
                    c.setFont("Helvetica", 12)

                    # Write the user name and count
                    c.drawString(x, y, user)
                    c.drawString(x + column_width, y, str(count))

                    rows_written += 1
                    y -= row_height  # Space between users

                    # Check if the maximum number of rows per page is reached
                    if rows_written >= max_rows_per_page:
                        # Create a new page
                        c.showPage()
                        # Reset the y-coordinate
                        y = 780
                        # Write the table headers
                        c.setFont("Helvetica-Bold", 12)
                        c.drawString(margin, 800, "User full name")
                        c.drawString(margin + column_width,
                                     800, "Count of Event name")
                        # Draw a horizontal line below the column headers
                        c.setStrokeColor(colors.darkblue)
                        c.setLineWidth(1)
                        c.line(margin, 795, margin + 2 * column_width, 795)
                        # Write the table content
                        c.setFont("Helvetica", 12)
                        rows_written = 0

                # Save the PDF file
                c.save()
                messagebox.showinfo(
                    "Success", "PDF file created successfully!")
            except Exception as e:
                messagebox.showerror(
                    "Error", f"An error occurred while generating the PDF file: {str(e)}")

        def main():
            try:
                csv_paths, pdf_path = get_file_paths()
                if not csv_paths or not pdf_path:
                    messagebox.showwarning(
                        "Warning", "No CSV files or output PDF file selected!")
                    return

                pivot_table, oldest_time_str, newest_time_str = process_csv_files(
                    csv_paths)
                if pivot_table is not None:
                    generate_pdf(pivot_table, pdf_path,
                                 oldest_time_str, newest_time_str)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        if __name__ == '__main__':
            main()
    except subprocess.CalledProcessError:
        print("Error occurred while executing shortened-alfa.py:",
              sys.exc_info()[0])
    else:
        window.destroy()  # Close the application after successful execution


def create_shortened_numeric_report():
    try:
        def get_file_paths():
            root = Tk()
            root.withdraw()

            # Prompt the user to select the CSV files
            csv_paths = filedialog.askopenfilenames(
                title='Select CSV Files', filetypes=[('CSV Files', '*.csv')])

            # Prompt the user to select the output PDF file path
            pdf_path = filedialog.asksaveasfilename(
                title='Save PDF File', defaultextension='.pdf', filetypes=[('PDF Files', '*.pdf')])

            return csv_paths, pdf_path

        def process_csv_files(csv_paths):
            try:
                dfs = []
                oldest_time = None
                newest_time = None

                for path in csv_paths:
                    df = pd.read_csv(path)

                    # Retrieve the oldest and newest time
                    time_col = df['Time']
                    if oldest_time is None or time_col.min() < oldest_time:
                        oldest_time = time_col.min()
                    if newest_time is None or time_col.max() > newest_time:
                        newest_time = time_col.max()

                    dfs.append(df)

                # Format the oldest and newest time as strings
                oldest_time_str = str(oldest_time)
                newest_time_str = str(newest_time)

                # Concatenate the DataFrames into a single DataFrame
                if len(dfs) > 0:
                    df = pd.concat(dfs)

                    # Perform the pivot table operation
                    pivot_table = df.pivot_table(
                        index='User full name', aggfunc='size', fill_value=0)

                    return pivot_table, oldest_time_str, newest_time_str
                else:
                    messagebox.showwarning("Warning", "No CSV files selected!")
                    return None, None, None
            except Exception as e:
                messagebox.showerror(
                    "Error", f"An error occurred while processing CSV files: {str(e)}")

        def generate_pdf(pivot_table, pdf_path, oldest_time_str, newest_time_str):
            try:
                # Create a new PDF document
                c = canvas.Canvas(pdf_path)

                # Set up the table layout
                row_height = 20
                column_width = 300
                margin = 50
                max_rows_per_page = 30  # Maximum number of rows per page

                # Write the time range as text in the PDF
                c.setFont("Helvetica-Bold", 13)
                c.drawString(
                    margin, 819, f"Attendance Report. From {oldest_time_str} to {newest_time_str}")

                # Sort the pivot table by the total count of event names
                pivot_table = pivot_table.sort_values()

                # Write the table headers
                c.setFont("Helvetica-Bold", 12)
                c.drawString(margin, 800, "User full name")
                c.drawString(margin + column_width, 800, "Count of Event name")

                # Draw a horizontal line below the column headers
                c.setStrokeColor(colors.darkblue)
                c.setLineWidth(1)
                c.line(margin, 795, margin + 2 * column_width, 795)

                # Write the table content
                c.setFont("Helvetica", 12)
                x = margin
                y = 780  # Adjust the initial y-coordinate to leave space for headers
                rows_written = 0
                for user, count in pivot_table.items():

                    # Check if the content exceeds the page height
                    if y < margin:
                        # Create a new page
                        c.showPage()
                        # Reset the y-coordinate
                        y = 780
                        # Write the table headers
                        c.setFont("Helvetica-Bold", 12)
                        c.drawString(margin, 800, "User full name")
                        c.drawString(margin + column_width,
                                     800, "Count of Event name")
                        # Draw a horizontal line below the column headers
                        c.setStrokeColor(colors.darkblue)
                        c.setLineWidth(1)
                        c.line(margin, 795, margin + 2 * column_width, 795)
                        # Write the table content
                        c.setFont("Helvetica", 12)

                    # Set the font to regular and black color for user name and count
                    c.setFillColor(colors.black)
                    c.setFont("Helvetica", 12)

                    # Write the user name and count
                    c.drawString(x, y, user)
                    c.drawString(x + column_width, y, str(count))

                    rows_written += 1
                    y -= row_height  # Space between users

                    # Check if the maximum number of rows per page is reached
                    if rows_written >= max_rows_per_page:
                        # Create a new page
                        c.showPage()
                        # Reset the y-coordinate
                        y = 780
                        # Write the table headers
                        c.setFont("Helvetica-Bold", 12)
                        c.drawString(margin, 800, "User full name")
                        c.drawString(margin + column_width,
                                     800, "Count of Event name")
                        # Draw a horizontal line below the column headers
                        c.setStrokeColor(colors.darkblue)
                        c.setLineWidth(1)
                        c.line(margin, 795, margin + 2 * column_width, 795)
                        # Write the table content
                        c.setFont("Helvetica", 12)
                        rows_written = 0

                # Save the PDF file
                c.save()
                messagebox.showinfo(
                    "Success", "PDF file created successfully!")
            except Exception as e:
                messagebox.showerror(
                    "Error", f"An error occurred while generating the PDF file: {str(e)}")

        def main():
            try:
                csv_paths, pdf_path = get_file_paths()
                if not csv_paths or not pdf_path:
                    messagebox.showwarning(
                        "Warning", "No CSV files or output PDF file selected!")
                    return

                pivot_table, oldest_time_str, newest_time_str = process_csv_files(
                    csv_paths)
                if pivot_table is not None:
                    generate_pdf(pivot_table, pdf_path,
                                 oldest_time_str, newest_time_str)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        if __name__ == '__main__':
            main()
    except subprocess.CalledProcessError:
        print("Error occurred while executing shortened-numeric.py:",
              sys.exc_info()[0])
    else:
        window.destroy()  # Close the application after successful execution


def create_extended_alfa_report():
    try:
        def get_file_paths():
            root = Tk()
            root.withdraw()

            # Prompt the user to select the CSV files
            csv_paths = filedialog.askopenfilenames(
                title='Select CSV Files', filetypes=[('CSV Files', '*.csv')])

            # Prompt the user to select the output PDF file path
            pdf_path = filedialog.asksaveasfilename(
                title='Save PDF File', defaultextension='.pdf', filetypes=[('PDF Files', '*.pdf')])

            return csv_paths, pdf_path

        def process_csv_files(csv_paths):
            try:
                dfs = []
                oldest_time = None
                newest_time = None

                for path in csv_paths:
                    df = pd.read_csv(path)

                    # Retrieve the oldest and newest time
                    time_col = df['Time']
                    if oldest_time is None or time_col.min() < oldest_time:
                        oldest_time = time_col.min()
                    if newest_time is None or time_col.max() > newest_time:
                        newest_time = time_col.max()

                    dfs.append(df)

                # Format the oldest and newest time as strings
                oldest_time_str = str(oldest_time)
                newest_time_str = str(newest_time)

                # Concatenate the DataFrames into a single DataFrame
                if len(dfs) > 0:
                    df = pd.concat(dfs)

                    # Perform the pivot table operation
                    pivot_table = df.pivot_table(
                        index='User full name', columns='Event name', aggfunc='size', fill_value=0)

                    return pivot_table, oldest_time_str, newest_time_str
                else:
                    messagebox.showwarning("Warning", "No CSV files selected!")
                    return None, None, None
            except Exception as e:
                messagebox.showerror(
                    "Error", f"An error occurred while processing CSV files: {str(e)}")

        def generate_pdf(pivot_table, pdf_path, oldest_time_str, newest_time_str):
            try:
                # Create a new PDF document
                c = canvas.Canvas(pdf_path)

                # Set up the table layout
                row_height = 20
                column_width = 250
                margin = 50
                max_rows_per_page = 30  # Maximum number of rows per page

                # Write the time range as text in the PDF
                c.setFont("Helvetica-Bold", 13)
                c.drawString(
                    margin, 819, f"Attendance Report. From {oldest_time_str} to {newest_time_str}")

                # Sort the pivot table alphabetically by User full name
                pivot_table = pivot_table.sort_index()

                # Write the table headers
                c.setFont("Helvetica-Bold", 12)
                c.drawString(margin, 800, "User full name")
                c.drawString(margin + column_width, 800, "Count of Event name")

                # Draw a horizontal line below the column headers
                c.setStrokeColor(colors.darkblue)
                c.setLineWidth(1)
                c.line(margin, 795, margin + 2 * column_width, 795)

                # Write the table content
                c.setFont("Helvetica", 12)
                x = margin
                y = 780  # Adjust the initial y-coordinate to leave space for headers
                rows_written = 0
                for user, row in pivot_table.iterrows():
                    # Exclude rows with "Count of Event name" value of 0, except when count of all event names is 0
                    if row.sum() == 0 and (row != 0).all():
                        continue

                    # Calculate the required space for the current user's data
                    # Number of non-zero rows + 1 for the user name
                    user_data_height = (len(row[row != 0]) + 1) * row_height

                    # Check if the content exceeds the page height
                    if y - user_data_height < margin:
                        # Create a new page
                        c.showPage()
                        # Reset the y-coordinate
                        y = 780
                        # Write the table headers
                        c.setFont("Helvetica-Bold", 12)
                        c.drawString(margin, 800, "User full name")
                        c.drawString(margin + column_width,
                                     800, "Count of Event name")
                        # Draw a horizontal line below the column headers
                        c.setStrokeColor(colors.darkblue)
                        c.setLineWidth(1)
                        c.line(margin, 795, margin + 2 * column_width, 795)
                        # Write the table content
                        c.setFont("Helvetica", 12)

                    # Set the font to bold and dark blue color for user name and count
                    c.setFillColor(colors.darkblue)
                    c.setFont("Helvetica-Bold", 12)

                    # Write the user name and count
                    c.drawString(x, y, user)
                    c.drawString(x + column_width, y, str(row.sum()))

                    # Reset the font to regular and black color for event names and counts
                    c.setFillColor(colors.black)
                    c.setFont("Helvetica", 12)

                    y -= row_height

                    # Write the event names and counts
                    for event, value in row.items():
                        if value != 0:
                            c.drawString(x, y, event)
                            c.drawString(x + column_width, y, str(value))
                            y -= row_height

                    rows_written += 1
                    y -= row_height  # Space between users

                    # Check if the maximum number of rows per page is reached
                    if rows_written >= max_rows_per_page:
                        # Create a new page
                        c.showPage()
                        # Reset the y-coordinate
                        y = 780
                        # Write the table headers
                        c.setFont("Helvetica-Bold", 12)
                        c.drawString(margin, 800, "User full name")
                        c.drawString(margin + column_width,
                                     800, "Count of Event name")
                        # Draw a horizontal line below the column headers
                        c.setStrokeColor(colors.darkblue)
                        c.setLineWidth(1)
                        c.line(margin, 795, margin + 2 * column_width, 795)
                        # Write the table content
                        c.setFont("Helvetica", 12)
                        rows_written = 0

                # Save the PDF file
                c.save()
                messagebox.showinfo(
                    "Success", "PDF file created successfully!")
            except Exception as e:
                messagebox.showerror(
                    "Error", f"An error occurred while generating the PDF file: {str(e)}")

        def main():
            try:
                csv_paths, pdf_path = get_file_paths()
                if not csv_paths or not pdf_path:
                    messagebox.showwarning(
                        "Warning", "No CSV files or output PDF file selected!")
                    return

                pivot_table, oldest_time_str, newest_time_str = process_csv_files(
                    csv_paths)
                if pivot_table is not None:
                    generate_pdf(pivot_table, pdf_path,
                                 oldest_time_str, newest_time_str)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        if __name__ == '__main__':
            main()
    except subprocess.CalledProcessError:
        print("Error occurred while executing extended-alfa.py:",
              sys.exc_info()[0])
    else:
        window.destroy()  # Close the application after successful execution


def create_extended_numeric_report():
    try:
        def get_file_paths():
            root = Tk()
            root.withdraw()

            # Prompt the user to select the CSV files
            csv_paths = filedialog.askopenfilenames(
                title='Select CSV Files', filetypes=[('CSV Files', '*.csv')])

            # Prompt the user to select the output PDF file path
            pdf_path = filedialog.asksaveasfilename(
                title='Save PDF File', defaultextension='.pdf', filetypes=[('PDF Files', '*.pdf')])

            return csv_paths, pdf_path

        def process_csv_files(csv_paths):
            try:
                dfs = []
                oldest_time = None
                newest_time = None

                for path in csv_paths:
                    df = pd.read_csv(path)

                    # Retrieve the oldest and newest time
                    time_col = df['Time']
                    if oldest_time is None or time_col.min() < oldest_time:
                        oldest_time = time_col.min()
                    if newest_time is None or time_col.max() > newest_time:
                        newest_time = time_col.max()

                    dfs.append(df)

                # Format the oldest and newest time as strings
                oldest_time_str = str(oldest_time)
                newest_time_str = str(newest_time)

                # Concatenate the DataFrames into a single DataFrame
                if len(dfs) > 0:
                    df = pd.concat(dfs)

                    # Perform the pivot table operation
                    pivot_table = df.pivot_table(
                        index='User full name', columns='Event name', aggfunc='size', fill_value=0)

                    return pivot_table, oldest_time_str, newest_time_str
                else:
                    messagebox.showwarning("Warning", "No CSV files selected!")
                    return None, None, None
            except Exception as e:
                messagebox.showerror(
                    "Error", f"An error occurred while processing CSV files: {str(e)}")

        def generate_pdf(pivot_table, pdf_path, oldest_time_str, newest_time_str):
            try:
                # Create a new PDF document
                c = canvas.Canvas(pdf_path)

                # Set up the table layout
                row_height = 20
                column_width = 250
                margin = 50
                max_rows_per_page = 30  # Maximum number of rows per page

                # Write the time range as text in the PDF
                c.setFont("Helvetica-Bold", 13)
                c.drawString(
                    margin, 819, f"Attendance Report. From {oldest_time_str} to {newest_time_str}")

                # Sort the pivot table by the total count of event names
                pivot_table = pivot_table.iloc[pivot_table.sum(
                    axis=1).argsort()]

                # Write the table headers
                c.setFont("Helvetica-Bold", 12)
                c.drawString(margin, 800, "User full name")
                c.drawString(margin + column_width, 800, "Count of Event name")

                # Draw a horizontal line below the column headers
                c.setStrokeColor(colors.darkblue)
                c.setLineWidth(1)
                c.line(margin, 795, margin + 2 * column_width, 795)

                # Write the table content
                c.setFont("Helvetica", 12)
                x = margin
                y = 780  # Adjust the initial y-coordinate to leave space for headers
                rows_written = 0
                for user, row in pivot_table.iterrows():
                    # Exclude rows with "Count of Event name" value of 0, except when count of all event names is 0
                    if row.sum() == 0 and (row != 0).all():
                        continue

                    # Calculate the required space for the current user's data
                    # Number of non-zero rows + 1 for the user name
                    user_data_height = (len(row[row != 0]) + 1) * row_height

                    # Check if the content exceeds the page height
                    if y - user_data_height < margin:
                        # Create a new page
                        c.showPage()
                        # Reset the y-coordinate
                        y = 780
                        # Write the table headers
                        c.setFont("Helvetica-Bold", 12)
                        c.drawString(margin, 800, "User full name")
                        c.drawString(margin + column_width,
                                     800, "Count of Event name")
                        # Draw a horizontal line below the column headers
                        c.setStrokeColor(colors.darkblue)
                        c.setLineWidth(1)
                        c.line(margin, 795, margin + 2 * column_width, 795)
                        # Write the table content
                        c.setFont("Helvetica", 12)

                    # Set the font to bold and dark blue color for user name and count
                    c.setFillColor(colors.darkblue)
                    c.setFont("Helvetica-Bold", 12)

                    # Write the user name and count
                    c.drawString(x, y, user)
                    c.drawString(x + column_width, y, str(row.sum()))

                    # Reset the font to regular and black color for event names and counts
                    c.setFillColor(colors.black)
                    c.setFont("Helvetica", 12)

                    y -= row_height

                    # Write the event names and counts
                    for event, value in row.items():
                        if value != 0:
                            c.drawString(x, y, event)
                            c.drawString(x + column_width, y, str(value))
                            y -= row_height

                    rows_written += 1
                    y -= row_height  # Space between users

                    # Check if the maximum number of rows per page is reached
                    if rows_written >= max_rows_per_page:
                        # Create a new page
                        c.showPage()
                        # Reset the y-coordinate
                        y = 780
                        # Write the table headers
                        c.setFont("Helvetica-Bold", 12)
                        c.drawString(margin, 800, "User full name")
                        c.drawString(margin + column_width,
                                     800, "Count of Event name")
                        # Draw a horizontal line below the column headers
                        c.setStrokeColor(colors.darkblue)
                        c.setLineWidth(1)
                        c.line(margin, 795, margin + 2 * column_width, 795)
                        # Write the table content
                        c.setFont("Helvetica", 12)
                        rows_written = 0

                # Save the PDF file
                c.save()
                messagebox.showinfo(
                    "Success", "PDF file created successfully!")
            except Exception as e:
                messagebox.showerror(
                    "Error", f"An error occurred while generating the PDF file: {str(e)}")

        def main():
            try:
                csv_paths, pdf_path = get_file_paths()
                if not csv_paths or not pdf_path:
                    messagebox.showwarning(
                        "Warning", "No CSV files or output PDF file selected!")
                    return

                pivot_table, oldest_time_str, newest_time_str = process_csv_files(
                    csv_paths)
                if pivot_table is not None:
                    generate_pdf(pivot_table, pdf_path,
                                 oldest_time_str, newest_time_str)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        if __name__ == '__main__':
            main()
    except subprocess.CalledProcessError:
        print("Error occurred while executing extended-numeric.py:",
              sys.exc_info()[0])
    else:
        window.destroy()  # Close the application after successful execution


def open_options_menu(option):
    # Clear the current window
    clear_window()

    if option == "Shortened":
        label_option_short = ttk.Label(window, text="Type of Report Selected: Shortened", font=(
            "Tahoma", 10), foreground="white", background='#1e1e1e')
        label_option_short.pack(pady=20)

        option1_button = ttk.Button(window, text="Sorted alphabetically",
                                    command=create_shortened_alfa_report, style="Custom.TButton")
        option1_button.pack(pady=10)

        option2_button = ttk.Button(window, text="Sorted by total number of events",
                                    command=create_shortened_numeric_report, style="Custom.TButton")
        option2_button.pack(pady=10)

        back_button = ttk.Button(
            window, text="←", command=create_main_menu, style="Custom.TButton")
        back_button.pack(pady=10)

    elif option == "Extended":
        label_option_extended = ttk.Label(window, text="Type of Report Selected: Extended", font=(
            "Tahoma", 10), foreground="white", background='#1e1e1e')
        label_option_extended.pack(pady=20)

        option1_button = ttk.Button(window, text="Sorted alphabetically",
                                    command=create_extended_alfa_report, style="Custom.TButton")
        option1_button.pack(pady=10)

        option2_button = ttk.Button(window, text="Sorted by total number of events",
                                    command=create_extended_numeric_report, style="Custom.TButton")
        option2_button.pack(pady=10)

        back_button = ttk.Button(
            window, text="←", command=create_main_menu, style="Custom.TButton")
        back_button.pack(pady=5)


def create_main_menu():
    # Clear the current window
    clear_window()

    title_label = ttk.Label(window, text="MOODLE LOGS SYNTHESIZER", font=(
        "Tahoma", 16, "bold"), foreground="white", background='#1e1e1e')
    title_label.pack(pady=20)

    below_label = ttk.Label(window, text="Select Report Type", font=(
        "Tahoma", 14), foreground="white", background='#1e1e1e')
    below_label.pack(pady=20)

    shortened_button = ttk.Button(window, text="Shortened", command=lambda: open_options_menu(
        "Shortened"), style="Custom.TButton")
    shortened_button.pack(pady=15)

    extended_button = ttk.Button(window, text="Extended", command=lambda: open_options_menu(
        "Extended"), style="Custom.TButton")
    extended_button.pack(pady=15)


def clear_window():
    # Clear the current contents of the window
    for widget in window.winfo_children():
        widget.destroy()


# Create the main window
window = tk.Tk()
window.title("Moodle Logs Synthesizer")

# Window Size
w = 600  # width for the Tk root
h = 285  # height for the Tk root

# get screen width and height
ws = window.winfo_screenwidth()  # width of the screen
hs = window.winfo_screenheight()  # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen
# and where it is placed
window.geometry('%dx%d+%d+%d' % (w, h, x, y))


# Apply a dark background
window.configure(bg='#1e1e1e')


# Apply a dark theme to the application
style = ttk.Style(window)
style.theme_use("clam")  # Choose the dark theme (you can try different themes)

# Configure the style for the buttons
style.configure(
    "Custom.TButton",
    foreground="white",
    background="#007acc",
    font=("Tahoma", 12),
    padding=10,
)


# Override the default theme colors for the selected button state
style.map(
    "Custom.TButton",
    foreground=[('pressed', 'white'), ('active', 'white')],
    background=[('pressed', '#009ccc'), ('active', '#009ccc')],
)


# Create the initial main menu
create_main_menu()

# Start the GUI event loop
window.mainloop()
