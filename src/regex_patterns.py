PATTERN_GPU = r"(RTX|GTX|RX)[-\s]*\d{4}[-\s]*(TI|Super|XTX|XT)?"
# Zur errinenrung (||) kann wörter unterscheiden und als option sehen
# [] kann nur ein einziges zeichen als option sehen
PATTERN_CPU_INTEL = r"(Intel Core)?\s?i[3579][-\s]*\d{4,5}(KF|F|K|T)?"
PATTERN_CPU_RYZEN = r"\b(Ryzen|R)\s?[3579][-\s]*\d{4}(x3d|xt|x|g)?"
PATTERN_RAM = r"(\d{1,2}\s*GB\s*(RAM|ARBEITSSPEICHER)|(RAM|ARBEITSSPEICHER):?\s*\d{1,2}\s*GB)|(\d{1,2}\s*GB\s*DDR[45])|(DDR[45][-\s]*\d{1,2}\s*GB)|(\d\s*x\s*\d{1,2}\s*GB\s*(ARBEITSSPEICHER|RAM|DDR[45])|DDR[45]\s*\d\s*x\s*\d{1,2}\s*GB)"
