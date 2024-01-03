# Generate Quarto Invoices

This is a simple script to generate biweekly invoices using Quarto/Typst.  
It first generates YAML files for each invoice, then generates the invoices from one single Quarto document.

## Usage

```bash
generate_invoices.py \
  --name="Consulting" \
  --task="A very important job" \
  --details="A description of the tasks" \
  --amount="1,234.56" \
  --recipient="Company-Inc" \
  --first="2024-01-15"\
  --last="2024-01-31" \
  --template="template.qmd"
```

Under the hood, this will generate a YAML file for each invoice, then generate the invoices from one single Quarto document using the `quarto render` command.

```bash
quarto render template.qmd --metadata-file input/202401-001.yml --output output/INVOICE-N202401-001-Company-Inc.pdf
```
