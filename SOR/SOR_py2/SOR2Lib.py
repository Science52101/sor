"""
Simple Object Reader 2 Library (SOR2Lib)
"""

from re import findall as _find
from json import dumps as _2json


def _SOread_line(objd: dict, line: str) -> dict:

  try:

    if '$' in line:
        for subst in _find(r'\$\S+\$', line): line = line.replace(subst, str(objd[subst.strip('$')]))

    sline: list[str] = [p.replace('*[ ', '').replace(' ]*', '') for p in _find('\*\[ .*? \]\*|\S+', line) if p]

    if sline[0].strip() == '...': return objd

    if len(sline) == 3: # 3-part operations

      [n, op, v] = sline

      if op in ['<::', 'xmv']: objd[n] = eval(v)
      elif op in ['<:<', 'nmv']: objd[n] = objd[v]

      elif op in ['<+:', 'xad']: objd[n] += eval(v)
      elif op in ['<+<', 'nad']: objd[n] += objd[v]

      elif op in ['<-:', 'xsb']: objd[n] -= eval(v)
      elif op in ['<-<', 'nsb']: objd[n] -= objd[v]

      elif op in ['<*:', 'xml']: objd[n] *= eval(v)
      elif op in ['<*<', 'nml']: objd[n] *= objd[v]

      elif op in ['</:', 'xdv']: objd[n] /= eval(v)
      elif op in ['</<', 'ndv']: objd[n] /= objd[v]

      elif op in ['<^:', 'xpw']: objd[n] **= eval(v)
      elif op in ['<^<', 'npw']: objd[n] **= objd[v]

      elif op in ['<%:', 'xmd']: objd[n] %= eval(v)
      elif op in ['<%<', 'nmd']: objd[n] %= objd[v]

      elif op in ['<&<', 'and']: objd[n] = objd[n] and objd[v]
      elif op in ['<|<', 'orr']: objd[n] = objd[n] or objd[v]

      elif op in ['<=:', 'xeq']: objd[n] = objd[n] == eval(v)
      elif op in ['<=<', 'neq']: objd[n] = objd[n] == objd[v]

      elif op in ['<!:', 'xxr']: objd[n] = objd[n] != eval(v)
      elif op in ['<!<', 'nxr']: objd[n] = objd[n] != objd[v]

    elif len(sline) == 6: # '-ets'

      if (sline[0] in ['let', 'set', 'def', 'define'] and
          sline[2] in [':', 'as', 'in', 'be'] and
          sline[4] in [':=', ':', '=', 'eq']):
        objd[sline[1]] = eval(sline[3])(eval(sline[5]))

    elif len(sline) == 2: # Directed operations

      if sline[0] in ['rm', 'remove', 'del', 'delete']: del objd[sline[1]]

    elif len(sline) == 4: # 'Gets'

      if (sline[0] in ['get', 'fetch', 'find'] and
          sline[2] in [':', 'from', ':<', 'gfrom']):
        nobjd: dict = objd
        for el in sline[3].split('\\'): nobjd = nobjd[el]
        objd[sline[1]] = nobjd[sline[1]]
        if sline[2] in [':<', 'gfrom']: del nobjd[sline[1]]

      elif (sline[0] in ['geta', 'fetcha', 'finda', 'getall', 'fetchall', 'findall'] and
          sline[2] in [':', 'from', ':<', 'gfrom']):
        nobjd: dict = objd
        for el in sline[3].split('\\'): nobjd = nobjd[el]
        for k in nobjd: objd[sline[1]+'_'+k] = nobjd[k]
        if sline[2] in [':<', 'gfrom']: del nobjd[sline[1]]

      elif (sline[0] in ['getf', 'fetchf', 'findf'] and
            sline[2] in [':', 'from']):
        p3: list[str] = sline[3].split('\\')
        nobjd: dict = SOread(open(p3[0]+'.sor2f', 'r').read())
        p3.remove(p3[0])
        for el in p3: nobjd = nobjd[el]
        objd[sline[1]] = nobjd[sline[1]]

    elif len(sline) == 1: # 'Magic words'

      if sline[0] in ['makeflat', 'mkflat']:
        for el in objd:
          if type(objd[el]) == dict:
            for elel in objd[el]: objd[elel] = objd[el][elel]

    return objd;
  except Exception as e:
    print(f'Error at line -- {line}')
    raise e


def SOread(objc: str, _objn: str = '', _d: int = 1, _pd : dict = {}) -> dict:
  """
  Read SO content from a string and return the SO data in a dictionary.

  Parameters
  ----------
  objc : str
    The object's content in a string.
  _objn : str, optional, default = ''
    The object's name.
  _d : int, optional, default = 1
    The `depth` of the object.
  _pd : dict, int, default =
    The previous data.

  Returns
  -------
  objd : dict
    The object's data in a dictionary.

  Notes
  -----
  Not using the SO2 syntax properly may result in many kinds of errors and poor functionality.

  The return o this function is not a SO, but a dictionary with its data.
  """

  objd: dict = _pd

  for comment in _find(r'\.\.\.\s+.+', objc): objc = objc.replace(comment, ' \n')

  objc = objc.replace('\n', ' ')

  if '**' in objc:
    eobjc: str
    eobjn: str
    eobjd: dict

    for eobjc in objc.split(' '+('**'*_d)+' '):
      if not eobjc.strip(): continue

      eobjn = eobjc.split(' '+('<<'*_d)+' ')[0].strip()
      eobjc = eobjc.split(' '+('<<'*_d)+' ')[1]
      eobjd = SOread(eobjc, eobjn, _d+1, objd if eobjn == 'OBJC' else {})

      if eobjn == 'OBJC':
        for el in eobjd: objd[el] = eobjd[el]
      else: objd[eobjn] = eobjd

  elif '--'*(_d-1) in objc:
    sobjc: list[str] = objc.split(('--'*(_d-1))+' ')
    for line in sobjc:
      if line.strip() not in ['', ' ']:
        if '&&&' in line and '...' != line.split()[0].strip():
          for sline in line.split('&&&'):
            objd = _SOread_line(objd, sline)
        objd = _SOread_line(objd, line)

  return objd


class SO:
  _data: dict

  def __init__(self) -> None: ...

  def make(self, **kwargs):
    """
    Get data from arguments.

    Parameters
    ----------
    **kwargs
      The arguments where the data is.

    Returns
    -------
    None
    """

    _data = kwargs

  def getfrom_str(self, source: str) -> None:
    """
    Get data from a string in SO2 syntax.

    Parameters
    ----------
    source : str
      The string where the data is in SO2 syntax.

    Returns
    -------
    None
    """

    self._data = SOread(source)

  def getfrom_dict(self, source: dict) -> None:
    """
    Get data from a python dictionary.

    Parameters
    ----------
    source : dict
      The dictionary where the data is.

    Returns
    -------
    None
    """

    self._data = source

  def get_data(self) -> dict:
    """
    Return the SO data as a dictionary.

    Returns
    -------
    _data : dict
      The SO data in a Python dictionary.
    """

    return self._data

  def get_json(self, **kwargs) -> str:
    """
    Return the SO data as a JSON string.

    Returns
    -------
    json_data : str
      The SO data in a JSON string.
    """

    return _2json(self._data, **kwargs)
