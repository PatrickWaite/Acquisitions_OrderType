import imports

def get_OrderInvoiceQuery(year,month):
    query = f"""
SELECT  
	orders.acquisitions_unit__t."name" as unitNAME,
	po_line__t.po_line_number,
	purchase_order__t__acq_unit_ids.date_ordered,
	organizations__t."name" as vendor,
	po_line__t.title_or_package as Title,
	po_line__t.order_format,
	po_line__t.selector,
	po_line__t.cost__po_line_estimated_price as encumbered_amount,
	invoice.invoice_lines__t.sub_total as expended_amount,
	finance.expense_class__t."name" as Expence_Class,
	fund__t__acq_unit_ids."name" as Fund_ID,
	po_line__t.details__receiving_note as receiving_notes,
	po_line__t.description as internal_notes,
	purchase_order__t__acq_unit_ids.workflow_status as PO_Status,
	invoices__t.status as Invoice_status
	
FROM orders.acquisitions_unit__t
join orders.purchase_order__t__acq_unit_ids on purchase_order__t__acq_unit_ids.acq_unit_ids = acquisitions_unit__t.id
join orders.po_line__t on po_line__t.purchase_order_id = purchase_order__t__acq_unit_ids.id

join orders.po_line__t__fund_distribution on po_line__t__fund_distribution.id = po_line__t.id 

join finance.fund__t__acq_unit_ids on fund__t__acq_unit_ids.id = po_line__t__fund_distribution.fund_distribution__fund_id
join finance.expense_class__t on expense_class__t.id = po_line__t__fund_distribution.fund_distribution__expense_class_id
join invoice.invoice_lines__t on invoice_lines__t.po_line_id = po_line__t.id
join invoice.invoices__t on invoices__t.id = invoice_lines__t.invoice_id

join organizations.organizations__t on organizations__t.id = purchase_order__t__acq_unit_ids.vendor
WHERE acquisitions_unit__t.name = 'UM'
and purchase_order__t__acq_unit_ids.date_ordered like '{year}-{month}%'
    """
    return query

def helloworld():
    print('Hello World')
    return 'World'