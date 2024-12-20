import locale

def formatCurrency(angka, with_prefix=False, desimal=2):
  try:
      locale.setlocale(locale.LC_NUMERIC, 'id_ID.UTF-8')
  except locale.Error:
      print("Locale id_ID.UTF-8 is not available.")
      return None
  rupiah = locale.format_string("%.*f", (desimal, angka), grouping=True)
  if with_prefix:
      return "Rp. {}".format(rupiah)
  
  return rupiah
