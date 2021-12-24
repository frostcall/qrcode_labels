'''
QR Code PDF Label Maker
v1.01 December 2021
Tom Howard

Updates:
Minor additions to comments.

Notes:
I had a bunch of 6-per page, 3 1/3" x 4" labels (Avery: 94215, 5164, and many others)
I also had a bunch of 30-per page, 1" x 2 5/8" labels (Avery: 5160, 8460 and others)

I wanted to create QR Codes to label moving boxes so I could use them with the 'QRbox' app for my phone.
That app allows you to bring your own codes 

Requirements: qrcode, fpdf
Install with: pip install qrcode && pip install fpdf
'''

import qrcode
from fpdf import FPDF
import os

##################################################################################################
#                                                                                                #
#         Make Changes to these variables below                                                  #
#                                                                                                #
#         5164 is 6-per page, 3 1/3" x 4" labels (Avery: 94215, 5164, and many others)           #
#         5160 is 30-per page, 1" x 2 5/8" labels (Avery: 5160, 8460 and others)                 #
##################################################################################################
paper = 5164                # Options are 5164 (6-per page) or 5160 (30 per page, 10 unique qr codes duplicated in each column)
line1 = "PROJECT"           # Make sure your app of choice can handle this part of the QRCode before wasting a print.
line2 = "(555) 459-2222"    # I used my phone number in case the boxes were lost
num_sheets = 10             # The number of sheets you want to print
start_num = 1               # Start label count at this number
##################################################################################################
##################################################################################################

pdf = FPDF('P','mm','Letter')
pdf.set_font('Arial')
pdf.set_font_size(14)

def select_sheet():
    if paper == 5164:
        labels_per_sheet = 6
    elif paper == 5160:
        labels_per_sheet = 10
    return labels_per_sheet

def place_tag(page_count,count,code):
        cimg = (f'{count}.png')
        if paper == 5164:
            if page_count == 1:         # First row, top left
                x = -5                  # Starting at 0 was still too far to the right so I started at -5.
                y = 20                  # All in mm
            elif page_count == 2:       # First row top right
                x = 110
                y = 20
            elif page_count == 3:       # 2nd row left
                x = -5
                y = 110
            elif page_count == 4:       # 2nd row right
                x = 110
                y = 110
            elif page_count == 5:       # 3rd row left
                x = -5
                y = 200
            elif page_count == 6:       # 3rd row right
                x = 110
                y = 200

            pdf.image(cimg,x,y-14,60,60,'PNG')
            pdf.text(x+60,y,code)       # print line1 + current count number (actual text of QR Code)
            pdf.text(x+60,y+10,line2)   # print line2
        elif paper == 5160:
            columns = 3
            x = 2
            y = (page_count * 27) - 12

            for i in range(columns):
                pdf.image(cimg,x,y-6,20,20,'PNG')
                pdf.text(x+20,y,code)       # print line1 + current count number (actual text of QR Code)
                pdf.text(x+20,y+10,line2)   # print line2
                x +=75

def main():
    count = start_num
    labels_per_sheet = select_sheet()
    for i in range(num_sheets):
        pdf.add_page()
        page_count = 1

        for i in range(labels_per_sheet):
            code = (f'{line1}_{count:04d}')
            print(f'Generated: {code}')
            img = qrcode.make(code)
            img.save(f'{count}.png')
            place_tag(page_count,count,code)
            os.remove(f'{count}.png')           # remove QR code PNG so it doesn't clutter up your folder.
            count += 1
            page_count += 1
    outfile = (f'labels_{line1}_{start_num:04d}-{count-1:04d}.pdf') 
    pdf.output(outfile, 'F')   
    print(f'Completed generating {num_sheets} sheets with a total of {count-1} labels.\n File saved as: {outfile}.')

if __name__ == "__main__":
    main()