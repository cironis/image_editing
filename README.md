# Installing Poppler for PDF Processing on Windows

Many Python PDF utilities (e.g., **`pdf2image`**) call the Poppler command-line tools  
(`pdfinfo.exe`, `pdftoppm.exe`, etc.).  
Follow the one-time setup below to install Poppler **inside this repo** under  
`tools\poppler-24.08.0`.

---

## 1️⃣  Download Poppler 24.08.0

    # PowerShell — ONE LINE
    Invoke-WebRequest `
      -Uri https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip `
      -OutFile poppler.zip

---

## 2️⃣  Extract into `tools\`

    Expand-Archive poppler.zip -DestinationPath tools\poppler-24.08.0 -Force

After extraction the key binaries are in:

    tools\poppler-24.08.0\Library\bin\pdfinfo.exe

*If you see an extra inner `poppler-24.08.0` folder, move its contents up one level so the path above is correct.*

---

## 3️⃣  Add Poppler’s **bin** folder to PATH

    setx PATH "%PATH%;%CD%\tools\poppler-24.08.0\Library\bin"

Close **all** terminals (or reload VS Code) so the updated PATH is picked up.

### Quick check

    pdfinfo -v        # should print “pdfinfo version 24.08.0 …”

---

## 4️⃣  Use Poppler in Python (`pdf2image` example)

    from pdf2image import convert_from_path
    import os

    POPPLER_BIN = os.path.abspath(r"tools\poppler-24.08.0\Library\bin")

    pages = convert_from_path(
        "assets/Brawler-v1.5-The-Void.pdf",
        first_page=4,
        last_page=4,
        poppler_path=POPPLER_BIN      # omit this if PATH already includes Poppler
    )

---

## 5️⃣  Troubleshooting

| Symptom / Error                                   | Likely Fix                                                             |
|---------------------------------------------------|------------------------------------------------------------------------|
| `PDFInfoNotInstalledError`                        | Poppler not on PATH **or** incorrect `poppler_path`.                   |
| `FileNotFoundError: pdfinfo.exe`                  | Check extraction path — confirm `pdfinfo.exe` exists as shown above.   |
| Command works in terminal but VS Code still hangs | Reload VS Code (`Ctrl + Shift + P → Reload Window`).                   |

---

**All set!** Once Poppler is on PATH (or passed via `poppler_path`) libraries like `pdf2image` will run without additional setup.
