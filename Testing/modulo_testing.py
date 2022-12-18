import unittest
import math
from Modelos.Plan import Plan


class TestCoordinacionesMethods(unittest.TestCase):

    def test_coordinaciones_base(self):
        alumnos = 30
        cupos = 30
        coordinaciones,cantidadAlumnos = estimarCoordinaciones(alumnos,cupos)
        self.assertEqual(1,coordinaciones)
    
    def test_coordinaciones_entrada_alumnos_invalida_string(self):
        alumnos = '30'
        cupos = 30
        coordinaciones,cantidadAlumnos = estimarCoordinaciones(alumnos,cupos)
        self.assertEqual(None,coordinaciones)
    
    def test_coordinaciones_entrada_alumnos_invalida_real(self):
        alumnos = 30.5
        cupos = 30
        coordinaciones,cantidadAlumnos = estimarCoordinaciones(alumnos,cupos)
        self.assertEqual(None,coordinaciones)

    def test_coodinaciones_entrada_cupos_invalida_string(self):
        alumnos = 30
        cupos = '30'
        coordinaciones,cantidadAlumnos = estimarCoordinaciones(alumnos,cupos)
        self.assertEqual(None,coordinaciones)

    def test_coodinaciones_entrada_cupos_invalida_real(self):
        alumnos = 30
        cupos = 15.5
        coordinaciones,cantidadAlumnos = estimarCoordinaciones(alumnos,cupos)
        self.assertEqual(None,coordinaciones)

    def test_coodinaciones_entradas_invalidas_strings(self):
        alumnos = '30'
        cupos = '30'
        coordinaciones,cantidadAlumnos = estimarCoordinaciones(alumnos,cupos)
        self.assertEqual(None,coordinaciones)

    def test_coodinaciones_entradas_invalidas_reales(self):
        alumnos = 30.5
        cupos = 30.5
        coordinaciones,cantidadAlumnos = estimarCoordinaciones(alumnos,cupos)
        self.assertEqual(None,coordinaciones)

    def test_coordinaciones_en_limite(self):
        alumnos = 33
        cupos = 30
        coordinaciones,cantidadAlumnos = estimarCoordinaciones(alumnos,cupos)
        self.assertEqual(1,coordinaciones)

    def test_coordinaciones_bajo_limite(self):
        alumnos = 32
        cupos = 30
        coordinaciones,cantidadAlumnos = estimarCoordinaciones(alumnos,cupos)
        self.assertEqual(1,coordinaciones)

    def test_coordinaciones_sobre_limite(self):
        alumnos = 34
        cupos = 30
        coordinaciones,cantidadAlumnos = estimarCoordinaciones(alumnos,cupos)
        self.assertEqual(2,coordinaciones)
    
    def test_coordinaciones_en_limite_2(self):
        alumnos = 11
        cupos = 10
        coordinaciones,cantidadAlumnos = estimarCoordinaciones(alumnos,cupos)
        self.assertEqual(1,coordinaciones)

    def test_coordinaciones_sobre_limite_2(self):
        alumnos = 12
        cupos = 10
        coordinaciones,cantidadAlumnos = estimarCoordinaciones(alumnos,cupos)
        self.assertEqual(2,coordinaciones)  

    def test_coordinaciones_en_limite_2(self):
        alumnos = 66
        cupos = 30
        coordinaciones,cantidadAlumnos = estimarCoordinaciones(alumnos,cupos)
        self.assertEqual(2,coordinaciones)  

    def test_coordinaciones_bajo_limite_2(self):
        alumnos = 65
        cupos = 30
        coordinaciones,cantidadAlumnos = estimarCoordinaciones(alumnos,cupos)
        self.assertEqual(2,coordinaciones)  

    def test_coordinaciones_sobre_limite_3(self):
        alumnos = 67
        cupos = 30
        coordinaciones,cantidadAlumnos = estimarCoordinaciones(alumnos,cupos)
        self.assertEqual(3,coordinaciones) 

    def test_periodo_anterior_segundo_semestre(self):
        ano = 2000
        semestre = 2
        anoAnterior,semestreAnterior = periodoAnterior(ano,semestre)
        self.assertEqual(anoAnterior,2000)
        self.assertEqual(semestreAnterior,1)

    def test_periodo_anterior_primer_semestre(self):
        ano = 2000
        semestre = 1
        anoAnterior,semestreAnterior = periodoAnterior(ano,semestre)
        self.assertEqual(anoAnterior,1999)
        self.assertEqual(semestreAnterior,2)

    def test_periodo_valido_primer_semestre(self):
        periodo = 1
        self.assertTrue(periodoValido(periodo))

    def test_periodo_valido_segundo_semestre(self):
        periodo = 2
        self.assertTrue(periodoValido(periodo))

    def test_periodo_invalido(self):
        periodo = 0
        self.assertFalse(periodoValido(periodo))

    def test_periodo_invalido_2(self):
        periodo = 4
        self.assertFalse(periodoValido(periodo))

    def test_periodo_invalido_string(self):
        periodo = "45"
        self.assertFalse(periodoValido(periodo))

    def test_ponderaciones_validas_1(self):
        valorHistorico = "50"
        valorPeriodoAnterior = "50"
        self.assertTrue(ponderacionesValidas(valorHistorico,valorPeriodoAnterior))

    def test_ponderaciones_validas_2(self):
        valorHistorico = "30"
        valorPeriodoAnterior = "70"
        self.assertTrue(ponderacionesValidas(valorHistorico,valorPeriodoAnterior))

    def test_ponderaciones_validas_3(self):
        valorHistorico = "80"
        valorPeriodoAnterior = "20"
        self.assertTrue(ponderacionesValidas(valorHistorico,valorPeriodoAnterior))

    def test_ponderaciones_invalidas_1(self):
        valorHistorico = "50.0"
        valorPeriodoAnterior = "50.0"
        self.assertFalse(ponderacionesValidas(valorHistorico,valorPeriodoAnterior))

    def test_ponderaciones_invalidas_2(self):
        valorHistorico = "text"
        valorPeriodoAnterior = "text"
        self.assertFalse(ponderacionesValidas(valorHistorico,valorPeriodoAnterior))
    
    def test_ponderaciones_invalidas_3(self):
        valorHistorico = "50"
        valorPeriodoAnterior = "text"
        self.assertFalse(ponderacionesValidas(valorHistorico,valorPeriodoAnterior))
    
    def test_ponderaciones_invalidas_4(self):
        valorHistorico = "text"
        valorPeriodoAnterior = "50"
        self.assertFalse(ponderacionesValidas(valorHistorico,valorPeriodoAnterior))

    def test_ponderaciones_invalidas_5(self):
        valorHistorico = "100"
        valorPeriodoAnterior = "1"
        self.assertFalse(ponderacionesValidas(valorHistorico,valorPeriodoAnterior))

    def test_ponderaciones_invalidas_5(self):
        valorHistorico = "-50"
        valorPeriodoAnterior = "150"
        self.assertFalse(ponderacionesValidas(valorHistorico,valorPeriodoAnterior))

    def test_ano_valido_1(self):
        ano = "2023"
        self.assertTrue(anoValido(ano))

    def test_ano_valido_2(self):
        ano = "2040"
        self.assertTrue(anoValido(ano))

    def test_ano_invalido_1(self):
        ano = "2010"
        self.assertFalse(anoValido(ano))

    def test_ano_invalido_2(self):
        ano = "text"
        self.assertFalse(anoValido(ano))

    def test_ano_invalido_3(self):
        ano = "4000"
        self.assertFalse(anoValido(ano))

    def test_ano_invalido_4(self):
        ano = ""
        self.assertFalse(anoValido(ano))

if __name__ == '__main__':
    unittest.main()


def estimarCoordinaciones(alumnos, cupos):
    if not isinstance(alumnos,int):
        return None,None
    if not isinstance(cupos,int):
        return None,None
    if alumnos < 0:
        return None,None
    if cupos <= 0:
        return None,None
    if alumnos == 0:
        return 0,0
    coords = math.ceil(alumnos/cupos)
    coordsMargen = coords-1
    margen = math.floor(cupos * 1.1)
    if coords == 1:
        return 1,alumnos
    else:
        alumnosMargen = math.ceil(alumnos/coordsMargen)
        if alumnosMargen <= margen:
            return coordsMargen,alumnosMargen
        return coords,math.ceil(alumnos/coords)

def periodoAnterior(ano, periodo):
    if periodo != 1 and periodo != 2:
        return None,None
    if periodo == 2:
        return ano, periodo - 1
    elif periodo == 1:
        return ano - 1, 2

def anoValido(ano):
    if not ano.isnumeric():
        return False
    ano = int(ano)
    if ano >= 2015 and ano <= 2050:
        return True

def periodoValido(periodo):
    if periodo == 1 or periodo == 2:
        return True
    return False

def tipoEstimacionValida(tipoEstimacion):
    if periodo == 1 or periodo == 2:
        return True

def ponderacionesValidas(ponderacionValoresHistoricos, ponderacionValoresPeriodoAnterior):
    if not ponderacionValoresHistoricos.isnumeric() or not ponderacionValoresPeriodoAnterior.isnumeric():
        return False
    valorHistorico = int(ponderacionValoresHistoricos)
    valorPeriodoAnterior = int(ponderacionValoresPeriodoAnterior)
    if valorHistorico + valorPeriodoAnterior != 100:
        return False
    return True