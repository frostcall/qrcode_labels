'''
QR Code PDF Label Maker
v1.0 December 2021
Tom Howard

Notes:
I had a bunch of 6-per page, 3 1/3" x 4" labels (Avery: 94215, 5164, and many others)
I wanted to create QR Codes to label moving boxes so I could use them with the 'QRbox' app for my phone.
That app allows you to bring your own codes 
'''

import qrcode
from fpdf import FPDF
import os

line1 = "PROJECT"           # Can't be more than 6 for 'QRbox'
line2 = "(555) 867-5309"    # I used my phone number in case the boxes were lost
num_sheets = 50             
labels_per_sheet = 6        # Currently only 6 works with my settings
start_num = 1               # Start label count at this number

count = start_num
pdf = FPDF('P','mm','Letter')
pdf.set_font('Arial')
pdf.set_font_size(14)

def place_tag(page_count,count,code):
        cimg = (f'{count}.png')
        
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
