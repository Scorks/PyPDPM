PyPDPM
===

.. image:: https://img.shields.io/pypi/v/icd.svg
    :target: https://pypi.python.org/pypi/icd
    :alt: Latest PyPI version


Tools for working with the CMS case-mix classification model, payment driven payment model (PDPM). Deatils about PDPM can be found here: `https://www.cms.gov/medicare/medicare-fee-for-service-payment/snfpps/pdpm`_.

If you are interested in helping contribute to this repository, or have any questions, feel free to `send me an email <carostrickland321@gmail.com>`_.

Usage
-----
Basic usage includes three primary tasks while dealing with PDPM HIPPS codes. 

- Retrieving reimbursement amounts for specific HIPPS codes
- Generating HIPPS codes from patient information
- Generating patient information from HIPPS codes

|
|

**PDPM Mappings**


Revenue per diem for Medicare patients is calculated through PDPM HIPPS codes. The table below summarizes each component of the HIPPS codes where columns 1 to 4 represent the payment groups for characters 1-4 (of five) in the PDPM HIPPS code.


+------------+------------+-----------+------------+------------+
| PT/OT Payment Group | SLP Payment Group  | Nursing Payment Group  |  NTA Payment Group  |  HIPPS Code Value   |
+============+============+===========+============+============+
|     TA     |     SA     |    ES3    |     NA     |      A     |
+------------+------------+-----------+------------+------------+
|     TB     |     SB     |    ES2    |     NB     |      B     |
+------------+------------+-----------+------------+------------+
|     TC     |     SC     |    ES1    |     NC     |      C     |
+------------+------------+-----------+------------+------------+
|     TD     |     SD     |    HDE2   |     ND     |      D     |
+------------+------------+-----------+------------+------------+
|     TE     |     SE     |    HDE1   |     NE     |      E     |
+------------+------------+-----------+------------+------------+
|     TF     |     SF     |    HBC2   |     NF     |      F     |
+------------+------------+-----------+------------+------------+
|     TG     |     SG     |    CBC2   |            |      G     |
+------------+------------+-----------+------------+------------+
|     TH     |     SH     |    CA2    |            |      H     |
+------------+------------+-----------+------------+------------+
|     TI     |     SI     |    CBC1   |            |      I     |
+------------+------------+-----------+------------+------------+
|     TJ     |     SJ     |    CA1    |            |      J     |
+------------+------------+-----------+------------+------------+
|     TK     |     SK     |    BAB2   |            |      K     |
+------------+------------+-----------+------------+------------+
|     TL     |     SL     |    BAB1   |            |      L     |
+------------+------------+-----------+------------+------------+
|     TM     |            |    HBC1   |            |      M     |
+------------+------------+-----------+------------+------------+
|     TN     |            |    LDE2   |            |      N     |
+------------+------------+-----------+------------+------------+
|     TO     |            |    LDE1   |            |      O     |
+------------+------------+-----------+------------+------------+
|     TP     |            |    LBC2   |            |      P     |
+------------+------------+-----------+------------+------------+
|            |            |    LBC1   |            |      Q     |
+------------+------------+-----------+------------+------------+
|            |            |    CDE2   |            |      R     |
+------------+------------+-----------+------------+------------+
|            |            |    CDE1   |            |      S     |
+------------+------------+-----------+------------+------------+
|            |            |    PDE2   |            |      T     |
+------------+------------+-----------+------------+------------+
|            |            |    PDE1   |            |      U     |
+------------+------------+-----------+------------+------------+
|            |            |    PBC2   |            |      V     |
+------------+------------+-----------+------------+------------+
|            |            |    PA2    |            |      W     |
+------------+------------+-----------+------------+------------+
|            |            |    PBC1   |            |      X     |
+------------+------------+-----------+------------+------------+
|            |            |    PA1    |            |      Y     |
+------------+------------+-----------+------------+------------+


The fifth character of the PDPM HIPPS code is based on the assessment type below.


+------------+-----------+
| Assessment Type | HIPPS Code Value |
+============+===========+
| Initial Patient Assessment | 0 |
+------------+-----------+
| PPS 5-Day Assessment |  1   |
+------------+-----------+
| Omnibus Budget Reconciliation Act |  6   |
+------------+-----------+
