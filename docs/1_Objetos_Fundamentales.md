{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "# Objetos Fundamentales"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "subslide"
    },
    "tags": []
   },
   "source": [
    "Para ejecutar todos los ejemplos se debe importar la librería. Se sugiere utilizar siempre el alias `qcf`. "
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:04:02.758431Z",
     "iopub.status.busy": "2024-07-08T12:04:02.758104Z",
     "iopub.status.idle": "2024-07-08T12:04:03.409331Z",
     "shell.execute_reply": "2024-07-08T12:04:03.408825Z",
     "shell.execute_reply.started": "2024-07-08T12:04:02.758404Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:26:09.906038Z",
     "start_time": "2025-06-06T11:26:09.902608Z"
    }
   },
   "source": [
    "import qcfinancial as qcf\n",
    "print(f\"Versión qcf en uso: {qcf.id()}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Versión en uso: version: 1.6.0, build: 2025-03-05 13:10\n"
     ]
    }
   ],
   "execution_count": 80
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "## Monedas"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Las divisas se representan con objetos de tipo `QCCurrency` y sus subclases. En estos momentos, de forma explícita, están implementadas las siguientes divisas:\n",
    "\n",
    "\n",
    "|  Lista | de  | Divisas  |\n",
    "|---|---|---|\n",
    "| AUD  | CNY  | JPY   |\n",
    "| BRL  | COP  | MXN  |\n",
    "| CAD   | DKK   | NOK   |\n",
    "| CHF  | EUR   | PEN  |\n",
    "| CLF  | GBP   | SEK  |\n",
    "| CLP  | HKD   | USD  |\n",
    "\n",
    "Si se requiere otra, solicitarlo ingresando un *issue* en el [git repo](https://github.com/qcfinancial/qcfinancial.git) del proyecto."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "El constructor por default retorna USD."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:04:03.411048Z",
     "iopub.status.busy": "2024-07-08T12:04:03.410614Z",
     "iopub.status.idle": "2024-07-08T12:04:03.414338Z",
     "shell.execute_reply": "2024-07-08T12:04:03.413735Z",
     "shell.execute_reply.started": "2024-07-08T12:04:03.411029Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:26.027547Z",
     "start_time": "2025-06-06T11:21:26.024366Z"
    }
   },
   "source": [
    "x = qcf.QCCurrency()\n",
    "print(f\"ISO Code: {x.get_iso_code()}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "ISO Code: USD\n"
     ]
    }
   ],
   "execution_count": 2
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Alta de divisas CLP, USD y JPY (USD se puede instanciar también de forma explícita)."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:04:03.415209Z",
     "iopub.status.busy": "2024-07-08T12:04:03.415014Z",
     "iopub.status.idle": "2024-07-08T12:04:03.418353Z",
     "shell.execute_reply": "2024-07-08T12:04:03.417720Z",
     "shell.execute_reply.started": "2024-07-08T12:04:03.415151Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:26.068835Z",
     "start_time": "2025-06-06T11:21:26.066078Z"
    }
   },
   "source": [
    "monedas = [\n",
    "    clp:=qcf.QCCLP(),\n",
    "    usd:=qcf.QCUSD(),\n",
    "    jpy:=qcf.QCJPY(),\n",
    "]"
   ],
   "outputs": [],
   "execution_count": 3
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Sin usar las subclases se puede instanciar una divisa que no esté implementada, por ejemplo para el peso argentino ARS:"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:04:03.420138Z",
     "iopub.status.busy": "2024-07-08T12:04:03.419962Z",
     "iopub.status.idle": "2024-07-08T12:04:03.423343Z",
     "shell.execute_reply": "2024-07-08T12:04:03.422670Z",
     "shell.execute_reply.started": "2024-07-08T12:04:03.420122Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:26.094086Z",
     "start_time": "2025-06-06T11:21:26.090721Z"
    }
   },
   "source": [
    "ars = qcf.QCCurrency('Peso argentino', 'ARS', 32, 0)\n",
    "monedas.append(ars)"
   ],
   "outputs": [],
   "execution_count": 4
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Métodos: `get_name`, `get_iso_code`, `get_iso_number`, `get_decimal_places` y `amount`."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "El método `amount`debe utilizarse cuando se debe pagar o recibir un monto resultado de un cálculo. De esta forma, el monto se redondea al número correcto de decimales en la divisa (que se obtiene con `get_decimal_places`). Por ejemplo, en CLP, se redondea a 0 decimales ya que en esta divisa no se utilizan los centavos."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:04:03.424233Z",
     "iopub.status.busy": "2024-07-08T12:04:03.424089Z",
     "iopub.status.idle": "2024-07-08T12:04:03.428283Z",
     "shell.execute_reply": "2024-07-08T12:04:03.427793Z",
     "shell.execute_reply.started": "2024-07-08T12:04:03.424218Z"
    },
    "slideshow": {
     "slide_type": "subslide"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:26.123643Z",
     "start_time": "2025-06-06T11:21:26.118322Z"
    }
   },
   "source": [
    "cantidad = 100.123456\n",
    "for moneda in monedas:\n",
    "    print(f\"Nombre: {format(moneda.get_name())}\")\n",
    "    print(f\"Código ISO: {moneda.get_iso_code()}\")\n",
    "    print(f\"Número ISO: {moneda.get_iso_number()}\")\n",
    "    print(f\"Número de decimales: {moneda.get_decimal_places()}\")\n",
    "    print(f\"Cantidad {cantidad} con el número correcto de decimales: {moneda.amount(cantidad):.4f}\")\n",
    "    print()"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Nombre: Chilean Peso\n",
      "Código ISO: CLP\n",
      "Número ISO: 152\n",
      "Número de decimales: 0\n",
      "Cantidad 100.123456 con el número correcto de decimales: 100.0000\n",
      "\n",
      "Nombre: U. S. Dollar\n",
      "Código ISO: USD\n",
      "Número ISO: 840\n",
      "Número de decimales: 2\n",
      "Cantidad 100.123456 con el número correcto de decimales: 100.1200\n",
      "\n",
      "Nombre: Japanese Yen\n",
      "Código ISO: JPY\n",
      "Número ISO: 392\n",
      "Número de decimales: 2\n",
      "Cantidad 100.123456 con el número correcto de decimales: 100.1200\n",
      "\n",
      "Nombre: Peso argentino\n",
      "Código ISO: ARS\n",
      "Número ISO: 32\n",
      "Número de decimales: 0\n",
      "Cantidad 100.123456 con el número correcto de decimales: 100.0000\n",
      "\n"
     ]
    }
   ],
   "execution_count": 5
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Más adelante, cuando veamos el concepto de índice, veremos como disponer de un objeto moneda simplifica la conversión de montos de una moneda a otra."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "## Fechas"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Las fechas se representan con objetos de tipo `QCDate`. Para inicializar un `QCDate` se requiere el día, el mes y el año de la fecha. También se puede inicializar sin valor (default constructor) en cuyo caso se obtendrá el 12-01-1969."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Constructores"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Inicializar sin valor."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:04:03.429632Z",
     "iopub.status.busy": "2024-07-08T12:04:03.429242Z",
     "iopub.status.idle": "2024-07-08T12:04:03.432837Z",
     "shell.execute_reply": "2024-07-08T12:04:03.432194Z",
     "shell.execute_reply.started": "2024-07-08T12:04:03.429613Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:26.217278Z",
     "start_time": "2025-06-06T11:21:26.212345Z"
    }
   },
   "source": [
    "fecha = qcf.QCDate()\n",
    "print(f\"Fecha: {fecha}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Fecha: 1969-01-12\n"
     ]
    }
   ],
   "execution_count": 6
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Inicializar con una fecha específica. En este caso, el contructor realiza una validación de los parámetros iniciales."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:04:03.433913Z",
     "iopub.status.busy": "2024-07-08T12:04:03.433772Z",
     "iopub.status.idle": "2024-07-08T12:04:03.437711Z",
     "shell.execute_reply": "2024-07-08T12:04:03.436790Z",
     "shell.execute_reply.started": "2024-07-08T12:04:03.433899Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:26.267262Z",
     "start_time": "2025-06-06T11:21:26.263797Z"
    }
   },
   "source": [
    "fecha1 = qcf.QCDate(14, 9, 2024)  # día, mes, año\n",
    "print(f\"Fecha: {fecha1}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Fecha: 2024-09-14\n"
     ]
    }
   ],
   "execution_count": 7
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Error al tratar de construir una fecha inválida."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:04:03.439372Z",
     "iopub.status.busy": "2024-07-08T12:04:03.438647Z",
     "iopub.status.idle": "2024-07-08T12:04:03.443665Z",
     "shell.execute_reply": "2024-07-08T12:04:03.443065Z",
     "shell.execute_reply.started": "2024-07-08T12:04:03.439352Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:26.343754Z",
     "start_time": "2025-06-06T11:21:26.337301Z"
    }
   },
   "source": [
    "try:\n",
    "    fecha0 = qcf.QCDate(31, 2, 2024)  # ¡¡¡ 31 de febrero !!!\n",
    "except ValueError as e:\n",
    "    print(e)"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Invalid day for month = 2\n"
     ]
    }
   ],
   "execution_count": 8
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": ""
    },
    "tags": []
   },
   "source": [
    "### Métodos `description`, `iso_code` y `__str__`"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:04:03.445025Z",
     "iopub.status.busy": "2024-07-08T12:04:03.444802Z",
     "iopub.status.idle": "2024-07-08T12:04:03.448081Z",
     "shell.execute_reply": "2024-07-08T12:04:03.447647Z",
     "shell.execute_reply.started": "2024-07-08T12:04:03.445008Z"
    },
    "slideshow": {
     "slide_type": ""
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:26.421943Z",
     "start_time": "2025-06-06T11:21:26.417548Z"
    }
   },
   "source": [
    "print(f\"description(True): {fecha.description(True)}\")\n",
    "print(f\"description(False): {fecha.description(False)}\")\n",
    "print(f\"iso_code(): {fecha.iso_code()}\")\n",
    "print(f\"__str__: {fecha}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "description(True): 12-01-1969\n",
      "description(False): 1969-01-12\n",
      "iso_code(): 1969-01-12\n",
      "__str__: 1969-01-12\n"
     ]
    }
   ],
   "execution_count": 9
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Getters y Setters"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Métodos: `set_day`, `set_month` y `set_year`."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:04:03.451096Z",
     "iopub.status.busy": "2024-07-08T12:04:03.450809Z",
     "iopub.status.idle": "2024-07-08T12:04:03.454909Z",
     "shell.execute_reply": "2024-07-08T12:04:03.454160Z",
     "shell.execute_reply.started": "2024-07-08T12:04:03.451079Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:26.519314Z",
     "start_time": "2025-06-06T11:21:26.514915Z"
    }
   },
   "source": [
    "fecha1.set_day(17)\n",
    "fecha1.set_month(10)\n",
    "fecha1.set_year(2024)\n",
    "print(f\"Fecha: {fecha1}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Fecha: 2024-10-17\n"
     ]
    }
   ],
   "execution_count": 10
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Métodos `day`, `month` y `year`."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:04:03.456516Z",
     "iopub.status.busy": "2024-07-08T12:04:03.456241Z",
     "iopub.status.idle": "2024-07-08T12:04:03.459808Z",
     "shell.execute_reply": "2024-07-08T12:04:03.459215Z",
     "shell.execute_reply.started": "2024-07-08T12:04:03.456498Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:26.574570Z",
     "start_time": "2025-06-06T11:21:26.570541Z"
    }
   },
   "source": [
    "print(f\"Día: {fecha1.day()}\")\n",
    "print(f\"Mes: {fecha1.month()}\")\n",
    "print(f\"Año: {fecha1.year()}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Día: 17\n",
      "Mes: 10\n",
      "Año: 2024\n"
     ]
    }
   ],
   "execution_count": 11
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": ""
    },
    "tags": []
   },
   "source": [
    "### Método `week_day`"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Retorna una variable de tipo `enum QC_Financial.WeekDay` que representa el día de la semana al que corresponde a la fecha."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:04:03.460706Z",
     "iopub.status.busy": "2024-07-08T12:04:03.460525Z",
     "iopub.status.idle": "2024-07-08T12:04:03.463834Z",
     "shell.execute_reply": "2024-07-08T12:04:03.463376Z",
     "shell.execute_reply.started": "2024-07-08T12:04:03.460690Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:26.677073Z",
     "start_time": "2025-06-06T11:21:26.672336Z"
    }
   },
   "source": [
    "dia_semana = fecha1.week_day()\n",
    "print(f\"Tipo del retorno: {type(dia_semana)}\")\n",
    "print(f\"Día de la semana: {dia_semana}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Tipo del retorno: <class 'qcfinancial.WeekDay'>\n",
      "Día de la semana: WeekDay.THU\n"
     ]
    }
   ],
   "execution_count": 12
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Método `add_months`"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Suma **n meses** a `fecha1` y retorna esa nueva fecha sin cambiar el valor de `fecha1`."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:04:03.464844Z",
     "iopub.status.busy": "2024-07-08T12:04:03.464649Z",
     "iopub.status.idle": "2024-07-08T12:04:03.468283Z",
     "shell.execute_reply": "2024-07-08T12:04:03.467821Z",
     "shell.execute_reply.started": "2024-07-08T12:04:03.464828Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:26.744905Z",
     "start_time": "2025-06-06T11:21:26.738934Z"
    }
   },
   "source": [
    "num_meses = 12\n",
    "fecha2 = fecha1.add_months(num_meses)\n",
    "print(f\"fecha1: {fecha1}\")\n",
    "print(f\"fecha2: {fecha2}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "fecha1: 2024-10-17\n",
      "fecha2: 2025-10-17\n"
     ]
    }
   ],
   "execution_count": 13
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Método `add_days`"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Suma **n días** a `fecha1` sin cambiar el valor de `fecha1`."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:04:03.469295Z",
     "iopub.status.busy": "2024-07-08T12:04:03.469112Z",
     "iopub.status.idle": "2024-07-08T12:04:03.473485Z",
     "shell.execute_reply": "2024-07-08T12:04:03.472676Z",
     "shell.execute_reply.started": "2024-07-08T12:04:03.469279Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:26.836447Z",
     "start_time": "2025-06-06T11:21:26.832471Z"
    }
   },
   "source": [
    "num_dias = 30\n",
    "fecha3 = fecha1.add_days(num_dias)\n",
    "print(f\"fecha1: {fecha1}\")\n",
    "print(f\"fecha3: {fecha3}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "fecha1: 2024-10-17\n",
      "fecha3: 2024-11-16\n"
     ]
    }
   ],
   "execution_count": 14
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Método `day_diff`"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Calcula la diferencia en días con otra fecha. Si la otra fecha es mayor el resultado es positivo, si no, es negativo."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:04:03.475014Z",
     "iopub.status.busy": "2024-07-08T12:04:03.474798Z",
     "iopub.status.idle": "2024-07-08T12:04:03.478269Z",
     "shell.execute_reply": "2024-07-08T12:04:03.477642Z",
     "shell.execute_reply.started": "2024-07-08T12:04:03.474994Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:26.902025Z",
     "start_time": "2025-06-06T11:21:26.897174Z"
    }
   },
   "source": [
    "# Dado que fecha3 > fecha1 entonces el resultado es positivo\n",
    "print(f\"fecha1.day_diff(fecha3): {fecha1.day_diff(fecha3)} (días)\")\n",
    "\n",
    "# Se invierten los roles y el resultado es negativo\n",
    "print(f\"fecha3.day_diff(fecha1): {fecha3.day_diff(fecha1)} (días)\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "fecha1.day_diff(fecha3): 30 (días)\n",
      "fecha3.day_diff(fecha1): -30 (días)\n"
     ]
    }
   ],
   "execution_count": 15
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Orden en `QCDate`"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "El orden de `QCDate` permite que las fechas pueden compararse entre si."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:04:03.479446Z",
     "iopub.status.busy": "2024-07-08T12:04:03.479247Z",
     "iopub.status.idle": "2024-07-08T12:04:03.483051Z",
     "shell.execute_reply": "2024-07-08T12:04:03.482559Z",
     "shell.execute_reply.started": "2024-07-08T12:04:03.479431Z"
    },
    "slideshow": {
     "slide_type": ""
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:27.008568Z",
     "start_time": "2025-06-06T11:21:27.002195Z"
    }
   },
   "source": [
    "print(f\"fecha1: {fecha1}\")\n",
    "print(f\"fecha2: {fecha2}\")\n",
    "print(f\"fecha1 == fecha2: {fecha1 == fecha2}\")\n",
    "print(f\"fecha1 != fecha2: {fecha1 != fecha2}\")\n",
    "print(f\"fecha1 < fecha2: {fecha1 < fecha2}\")\n",
    "print(f\"fecha1 <= fecha2: {fecha1 <= fecha2}\")\n",
    "print(f\"fecha1 > fecha2: {fecha1 > fecha2}\")\n",
    "print(f\"fecha1 >= fecha2: {fecha1 >= fecha2}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "fecha1: 2024-10-17\n",
      "fecha2: 2025-10-17\n",
      "fecha1 == fecha2: False\n",
      "fecha1 != fecha2: True\n",
      "fecha1 < fecha2: True\n",
      "fecha1 <= fecha2: True\n",
      "fecha1 > fecha2: False\n",
      "fecha1 >= fecha2: False\n"
     ]
    }
   ],
   "execution_count": 16
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Un objeto `QCDate` es *hashable*"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Esto permite que las fechas puedan usarse como `key` en un `dict`de Python. El hash que se utiliza coincide con la representación como entero de una fecha que se utiliza en Excel."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:04:03.484722Z",
     "iopub.status.busy": "2024-07-08T12:04:03.484374Z",
     "iopub.status.idle": "2024-07-08T12:04:03.488466Z",
     "shell.execute_reply": "2024-07-08T12:04:03.487296Z",
     "shell.execute_reply.started": "2024-07-08T12:04:03.484704Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:27.085501Z",
     "start_time": "2025-06-06T11:21:27.080569Z"
    }
   },
   "source": [
    "print(fecha1.__hash__())"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "45582\n"
     ]
    }
   ],
   "execution_count": 17
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Por ejemplo, una serie de tiempo:"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:04:03.490623Z",
     "iopub.status.busy": "2024-07-08T12:04:03.490271Z",
     "iopub.status.idle": "2024-07-08T12:04:03.494686Z",
     "shell.execute_reply": "2024-07-08T12:04:03.494187Z",
     "shell.execute_reply.started": "2024-07-08T12:04:03.490605Z"
    },
    "slideshow": {
     "slide_type": "subslide"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:27.172538Z",
     "start_time": "2025-06-06T11:21:27.167478Z"
    }
   },
   "source": [
    "serie_de_tiempo = {\n",
    "    qcf.QCDate(22, 5, 2024): 100.01,\n",
    "    qcf.QCDate(23, 5, 2024): 100.02,\n",
    "    qcf.QCDate(24, 5, 2024): 100.03,\n",
    "}\n",
    "print(f\"Valor al: {qcf.QCDate(23, 5, 2024)} es {serie_de_tiempo[qcf.QCDate(23, 5, 2024)]}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Valor al: 2024-05-23 es 100.02\n"
     ]
    }
   ],
   "execution_count": 18
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Método `build_qcdate_from_string`"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Se trata de un *factory method* que permite inicializar un objeto `QCDate` a partir de un `string`.\n",
    "El formato del `string` debe ser yyyy&mm&dd donde & es un separador arbitrario."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:04:03.495654Z",
     "iopub.status.busy": "2024-07-08T12:04:03.495503Z",
     "iopub.status.idle": "2024-07-08T12:04:03.499434Z",
     "shell.execute_reply": "2024-07-08T12:04:03.498837Z",
     "shell.execute_reply.started": "2024-07-08T12:04:03.495638Z"
    },
    "scrolled": true,
    "slideshow": {
     "slide_type": ""
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:27.248217Z",
     "start_time": "2025-06-06T11:21:27.242030Z"
    }
   },
   "source": [
    "str1 = \"2020-01-01\"\n",
    "str2 = \"2020/01/02\"\n",
    "str3 = \"2020&01&03\"\n",
    "\n",
    "fecha4 = qcf.build_qcdate_from_string(str1)\n",
    "print(f\"{str1}: {fecha4}\")\n",
    "\n",
    "fecha4 = qcf.build_qcdate_from_string(str2)\n",
    "print(f\"{str2}: {fecha4}\")\n",
    "\n",
    "fecha4 = qcf.build_qcdate_from_string(str3)\n",
    "print(f\"{str3}: {fecha4}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2020-01-01: 2020-01-01\n",
      "2020/01/02: 2020-01-02\n",
      "2020&01&03: 2020-01-03\n"
     ]
    }
   ],
   "execution_count": 19
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "## Calendarios"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-01T12:07:17.570743Z",
     "iopub.status.busy": "2024-07-01T12:07:17.570335Z",
     "iopub.status.idle": "2024-07-01T12:07:17.578122Z",
     "shell.execute_reply": "2024-07-01T12:07:17.576844Z",
     "shell.execute_reply.started": "2024-07-01T12:07:17.570713Z"
    },
    "slideshow": {
     "slide_type": "subslide"
    },
    "tags": []
   },
   "source": [
    "Para construir correctamente la tabla de desarrollo de un bono o de las patas de un swap, es necesario conocer los calendarios que se debe aplicar en cada caso. \n",
    "\n",
    "Sólo así es posible determinar qué fechas de pago, de inicio y fin de devengo y otras son admisibles."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-07T11:30:55.950395Z",
     "iopub.status.busy": "2024-07-07T11:30:55.950094Z",
     "iopub.status.idle": "2024-07-07T11:30:55.959768Z",
     "shell.execute_reply": "2024-07-07T11:30:55.958599Z",
     "shell.execute_reply.started": "2024-07-07T11:30:55.950367Z"
    },
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Los calendarios se representan con objetos de tipo `BusinesssCalendar` y son **listas** de fechas arbitrarias que representan días feriados en alguna ciudad, país, región o unión de las anteriores. "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Para dar de alta un calendario se requiere:\n",
    "\n",
    "- una fecha inicial (`QCDate`)\n",
    "- y un número entero positivo que representa el plazo inicial total del calendario en años."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "El objeto `BusinessCalendar` incluye explícitamente todos los días 1 de enero y considera siempre como feriado los días sábado y domingo (aunque no pertenecen de forma explícita a la **lista**)."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "En el siguiente loop, por ejemplo, no se imprime nada."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:08:41.687906Z",
     "iopub.status.busy": "2024-07-08T12:08:41.687649Z",
     "iopub.status.idle": "2024-07-08T12:08:41.691565Z",
     "shell.execute_reply": "2024-07-08T12:08:41.690809Z",
     "shell.execute_reply.started": "2024-07-08T12:08:41.687886Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:27.345486Z",
     "start_time": "2025-06-06T11:21:27.341199Z"
    }
   },
   "source": [
    "fecha_inicio_calendario = qcf.QCDate(1, 1, 2024)\n",
    "scl = qcf.BusinessCalendar(fecha1, 10)"
   ],
   "outputs": [],
   "execution_count": 20
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:08:41.955129Z",
     "iopub.status.busy": "2024-07-08T12:08:41.954772Z",
     "iopub.status.idle": "2024-07-08T12:08:41.960983Z",
     "shell.execute_reply": "2024-07-08T12:08:41.960013Z",
     "shell.execute_reply.started": "2024-07-08T12:08:41.955106Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:27.388671Z",
     "start_time": "2025-06-06T11:21:27.385316Z"
    }
   },
   "source": [
    "for holiday in scl.get_holidays():\n",
    "    print(holiday)"
   ],
   "outputs": [],
   "execution_count": 21
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Método `add_holiday`"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Agrega una fecha a la lista."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:08:42.895096Z",
     "iopub.status.busy": "2024-07-08T12:08:42.894840Z",
     "iopub.status.idle": "2024-07-08T12:08:42.898809Z",
     "shell.execute_reply": "2024-07-08T12:08:42.897877Z",
     "shell.execute_reply.started": "2024-07-08T12:08:42.895077Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:27.424509Z",
     "start_time": "2025-06-06T11:21:27.421184Z"
    }
   },
   "source": [
    "scl.add_holiday(qcf.QCDate(18, 9, 2024))"
   ],
   "outputs": [],
   "execution_count": 22
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:08:43.253666Z",
     "iopub.status.busy": "2024-07-08T12:08:43.253417Z",
     "iopub.status.idle": "2024-07-08T12:08:43.258152Z",
     "shell.execute_reply": "2024-07-08T12:08:43.257172Z",
     "shell.execute_reply.started": "2024-07-08T12:08:43.253645Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:27.475637Z",
     "start_time": "2025-06-06T11:21:27.471255Z"
    }
   },
   "source": [
    "for holiday in scl.get_holidays():\n",
    "    print(holiday)"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2024-09-18\n"
     ]
    }
   ],
   "execution_count": 23
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Método `next_busy_day`"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Dada una fecha, si ésta es hábil retorna la misma fecha, si, por el contrario, la fecha es inhábil, devuelve la siguiente fecha hábil del calendario."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Veamos qué ocurre si aplicamos este método al 18-09-2024, fecha que acabamos de incluir."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:08:44.537536Z",
     "iopub.status.busy": "2024-07-08T12:08:44.537103Z",
     "iopub.status.idle": "2024-07-08T12:08:44.541670Z",
     "shell.execute_reply": "2024-07-08T12:08:44.540683Z",
     "shell.execute_reply.started": "2024-07-08T12:08:44.537510Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:27.534765Z",
     "start_time": "2025-06-06T11:21:27.529482Z"
    }
   },
   "source": [
    "print(f\"Next para el {(sept18 := qcf.QCDate(18, 9, 2024))}: {scl.next_busy_day(sept18)}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Next para el 2024-09-18: 2024-09-19\n"
     ]
    }
   ],
   "execution_count": 24
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Agregamos ahora el 19-09-2024 y vemos el nuevo resultado."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:08:45.000964Z",
     "iopub.status.busy": "2024-07-08T12:08:45.000640Z",
     "iopub.status.idle": "2024-07-08T12:08:45.006175Z",
     "shell.execute_reply": "2024-07-08T12:08:45.005217Z",
     "shell.execute_reply.started": "2024-07-08T12:08:45.000939Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:27.608520Z",
     "start_time": "2025-06-06T11:21:27.603571Z"
    }
   },
   "source": [
    "print(\"Se agrega el 19-9-2024 a la lista\")\n",
    "scl.add_holiday(qcf.QCDate(19, 9, 2024))\n",
    "next = scl.next_busy_day(qcf.QCDate(18, 9, 2024))\n",
    "print(f\"Nuevo next para el {sept18}: {next.week_day()}, {next}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Se agrega el 19-9-2024 a la lista\n",
      "Nuevo next para el 2024-09-18: WeekDay.FRI, 2024-09-20\n"
     ]
    }
   ],
   "execution_count": 25
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Pero el 2024, el 20 de septiembre también es feriado. Incluyámoslo y veamos el efecto."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:08:45.654158Z",
     "iopub.status.busy": "2024-07-08T12:08:45.653898Z",
     "iopub.status.idle": "2024-07-08T12:08:45.658955Z",
     "shell.execute_reply": "2024-07-08T12:08:45.658217Z",
     "shell.execute_reply.started": "2024-07-08T12:08:45.654126Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:27.691647Z",
     "start_time": "2025-06-06T11:21:27.687029Z"
    }
   },
   "source": [
    "print(\"Se agrega el 20-9-2024 a la lista\")\n",
    "scl.add_holiday(qcf.QCDate(20, 9, 2024))\n",
    "next = scl.next_busy_day(qcf.QCDate(18, 9, 2024))\n",
    "print(f\"Nuevo next para el {sept18}: {next.week_day()}, {next}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Se agrega el 20-9-2024 a la lista\n",
      "Nuevo next para el 2024-09-18: WeekDay.MON, 2024-09-23\n"
     ]
    }
   ],
   "execution_count": 26
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Método `mod_next_busy_day`"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Opera igual que la función anterior a menos que ésta retorne una fecha del mes siguiente, en ese caso retorna la fecha hábil anterior."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Probemos el comportamiento usando el 30-04-2024."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:08:46.849951Z",
     "iopub.status.busy": "2024-07-08T12:08:46.849714Z",
     "iopub.status.idle": "2024-07-08T12:08:46.853830Z",
     "shell.execute_reply": "2024-07-08T12:08:46.853032Z",
     "shell.execute_reply.started": "2024-07-08T12:08:46.849934Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:27.770887Z",
     "start_time": "2025-06-06T11:21:27.766742Z"
    }
   },
   "source": [
    "abril30 = qcf.QCDate(30, 4, 2024)\n",
    "print(f\"Abril 30: {abril30.week_day()}, {abril30}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Abril 30: WeekDay.TUE, 2024-04-30\n"
     ]
    }
   ],
   "execution_count": 27
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Vemos que es un martes y no es feriado, por lo tanto al aplicar `next_busy_day` no hay cambio de fecha:"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:08:47.565283Z",
     "iopub.status.busy": "2024-07-08T12:08:47.565024Z",
     "iopub.status.idle": "2024-07-08T12:08:47.568697Z",
     "shell.execute_reply": "2024-07-08T12:08:47.567914Z",
     "shell.execute_reply.started": "2024-07-08T12:08:47.565260Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:27.845301Z",
     "start_time": "2025-06-06T11:21:27.840455Z"
    }
   },
   "source": [
    "print(f\"Next para el {abril30}: {scl.next_busy_day(abril30)}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Next para el 2024-04-30: 2024-04-30\n"
     ]
    }
   ],
   "execution_count": 28
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Ahora, si lo agregamos al calendario, sí se produce el cambio de fecha."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:08:48.042446Z",
     "iopub.status.busy": "2024-07-08T12:08:48.042180Z",
     "iopub.status.idle": "2024-07-08T12:08:48.046389Z",
     "shell.execute_reply": "2024-07-08T12:08:48.045488Z",
     "shell.execute_reply.started": "2024-07-08T12:08:48.042425Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:27.920547Z",
     "start_time": "2025-06-06T11:21:27.916110Z"
    }
   },
   "source": [
    "scl.add_holiday(abril30)\n",
    "print(f\"Next para el {abril30}: {scl.next_busy_day(abril30)}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Next para el 2024-04-30: 2024-05-01\n"
     ]
    }
   ],
   "execution_count": 29
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Y vemos además que nos cambiamos de mes, pero si aplicamos `mod_next_busy_day` vemos que el resultado es el día hábil anterior."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:08:48.783473Z",
     "iopub.status.busy": "2024-07-08T12:08:48.783196Z",
     "iopub.status.idle": "2024-07-08T12:08:48.787371Z",
     "shell.execute_reply": "2024-07-08T12:08:48.786494Z",
     "shell.execute_reply.started": "2024-07-08T12:08:48.783448Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:27.988939Z",
     "start_time": "2025-06-06T11:21:27.984813Z"
    }
   },
   "source": [
    "print(f\"Mod next para el {abril30}: {scl.mod_next_busy_day(abril30)}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Mod next para el 2024-04-30: 2024-04-29\n"
     ]
    }
   ],
   "execution_count": 30
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Método `prev_busy_day`"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Opera de forma análoga a `busy_day`, pero retornando la fecha hábil anterior."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:08:50.235308Z",
     "iopub.status.busy": "2024-07-08T12:08:50.235046Z",
     "iopub.status.idle": "2024-07-08T12:08:50.238953Z",
     "shell.execute_reply": "2024-07-08T12:08:50.238009Z",
     "shell.execute_reply.started": "2024-07-08T12:08:50.235288Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:28.071337Z",
     "start_time": "2025-06-06T11:21:28.067234Z"
    }
   },
   "source": [
    "print(\"prev:\", scl.prev_busy_day(abril30))"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "prev: 2024-04-29\n"
     ]
    }
   ],
   "execution_count": 31
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Método `shift`"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Suma un número *n* (positivo o negativo) de días hábiles a una fecha."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Veamos algunos ejemplos."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:08:51.576270Z",
     "iopub.status.busy": "2024-07-08T12:08:51.576005Z",
     "iopub.status.idle": "2024-07-08T12:08:51.581030Z",
     "shell.execute_reply": "2024-07-08T12:08:51.580169Z",
     "shell.execute_reply.started": "2024-07-08T12:08:51.576247Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:28.134570Z",
     "start_time": "2025-06-06T11:21:28.129162Z"
    }
   },
   "source": [
    "print(f\"Fecha inicial: {abril30}\")\n",
    "shifted = scl.shift(abril30, 0)\n",
    "print(f\"n = 0, {shifted.week_day()}, {shifted}\")\n",
    "\n",
    "shifted = scl.shift(abril30, 1)\n",
    "print(f\"n = 1, {shifted.week_day()}, {shifted}\")\n",
    "\n",
    "shifted = scl.shift(abril30, 5)\n",
    "print(f\"n = 5, {shifted.week_day()}, {shifted}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Fecha inicial: 2024-04-30\n",
      "n = 0, WeekDay.TUE, 2024-04-30\n",
      "n = 1, WeekDay.WED, 2024-05-01\n",
      "n = 5, WeekDay.TUE, 2024-05-07\n"
     ]
    }
   ],
   "execution_count": 32
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Veamos en particular qué ocurre cuando usamos un número negativo."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:08:52.778427Z",
     "iopub.status.busy": "2024-07-08T12:08:52.778146Z",
     "iopub.status.idle": "2024-07-08T12:08:52.782381Z",
     "shell.execute_reply": "2024-07-08T12:08:52.781476Z",
     "shell.execute_reply.started": "2024-07-08T12:08:52.778405Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:28.225561Z",
     "start_time": "2025-06-06T11:21:28.221660Z"
    }
   },
   "source": [
    "mayo2 = qcf.QCDate(2, 5, 2024)\n",
    "print(f\"n = -1: {scl.shift(mayo2, -1)}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "n = -1: 2024-05-01\n"
     ]
    }
   ],
   "execution_count": 33
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Agreguemos el 2024-05-01 a los feriados de `scl` y veamos cómo cambia el primer resultado."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:08:53.735362Z",
     "iopub.status.busy": "2024-07-08T12:08:53.735054Z",
     "iopub.status.idle": "2024-07-08T12:08:53.740011Z",
     "shell.execute_reply": "2024-07-08T12:08:53.739104Z",
     "shell.execute_reply.started": "2024-07-08T12:08:53.735336Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:28.316194Z",
     "start_time": "2025-06-06T11:21:28.312070Z"
    }
   },
   "source": [
    "scl.add_holiday(qcf.QCDate(1, 5, 2024))\n",
    "print(f\"n = -1: {scl.shift(mayo2, -1)}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "n = -1: 2024-04-29\n"
     ]
    }
   ],
   "execution_count": 34
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Se va al 29 de abril porque también agregamos como feriado el 30 de abril."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Integración con `holidays`"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "`holidays` es una muy buena librería en Python puro que provee los feriados de más de 100 países, ciudades y mercados. Cuando no se está conectado a una BBDD y se quiere dar de alta un calendario, integrar `holidays` con `qcf.BusinessCalendar` es una muy buena opción."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "En el siguiente ejemplo, se construye el calendario de Santiago."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:32:50.539912Z",
     "iopub.status.busy": "2024-07-08T12:32:50.539583Z",
     "iopub.status.idle": "2024-07-08T12:32:50.542997Z",
     "shell.execute_reply": "2024-07-08T12:32:50.542355Z",
     "shell.execute_reply.started": "2024-07-08T12:32:50.539890Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:28.419963Z",
     "start_time": "2025-06-06T11:21:28.389787Z"
    }
   },
   "source": [
    "import holidays as hol"
   ],
   "outputs": [],
   "execution_count": 35
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:32:51.040554Z",
     "iopub.status.busy": "2024-07-08T12:32:51.040243Z",
     "iopub.status.idle": "2024-07-08T12:32:51.075096Z",
     "shell.execute_reply": "2024-07-08T12:32:51.074420Z",
     "shell.execute_reply.started": "2024-07-08T12:32:51.040528Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:28.653568Z",
     "start_time": "2025-06-06T11:21:28.450945Z"
    }
   },
   "source": "hol_scl = us_holidays = hol.CL(years=range(2024, 2045))",
   "outputs": [],
   "execution_count": 36
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Vemos que `scl` es un objeto similar a un Python `dict`."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:32:51.520390Z",
     "iopub.status.busy": "2024-07-08T12:32:51.520060Z",
     "iopub.status.idle": "2024-07-08T12:32:51.524429Z",
     "shell.execute_reply": "2024-07-08T12:32:51.523631Z",
     "shell.execute_reply.started": "2024-07-08T12:32:51.520363Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:28.670364Z",
     "start_time": "2025-06-06T11:21:28.665542Z"
    }
   },
   "source": [
    "for i, d in enumerate(hol_scl.items()):\n",
    "    if i < 10:\n",
    "        print(d[0], d[1])"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2024-01-01 New Year's Day\n",
      "2024-03-29 Good Friday\n",
      "2024-03-30 Holy Saturday\n",
      "2024-05-01 Labor Day\n",
      "2024-05-21 Navy Day\n",
      "2024-06-20 National Day of Indigenous Peoples\n",
      "2024-06-29 Saint Peter and Saint Paul's Day\n",
      "2024-07-16 Our Lady of Mount Carmel\n",
      "2024-08-15 Assumption Day\n",
      "2024-09-18 Independence Day\n"
     ]
    }
   ],
   "execution_count": 37
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Damos de alta un objeto de tipo `qcf.BusinessCalendar`."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:32:52.295209Z",
     "iopub.status.busy": "2024-07-08T12:32:52.294791Z",
     "iopub.status.idle": "2024-07-08T12:32:52.298141Z",
     "shell.execute_reply": "2024-07-08T12:32:52.297459Z",
     "shell.execute_reply.started": "2024-07-08T12:32:52.295187Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:28.716542Z",
     "start_time": "2025-06-06T11:21:28.713329Z"
    }
   },
   "source": [
    "qcf_scl = qcf.BusinessCalendar(qcf.QCDate(1, 2, 2024), 20)"
   ],
   "outputs": [],
   "execution_count": 38
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Y luego lo poblamos con las fechas de `scl`."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T12:32:52.742583Z",
     "iopub.status.busy": "2024-07-08T12:32:52.742304Z",
     "iopub.status.idle": "2024-07-08T12:32:52.746990Z",
     "shell.execute_reply": "2024-07-08T12:32:52.746291Z",
     "shell.execute_reply.started": "2024-07-08T12:32:52.742561Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:28.752080Z",
     "start_time": "2025-06-06T11:21:28.745798Z"
    }
   },
   "source": [
    "for d in hol_scl.keys():\n",
    "    qcf_scl.add_holiday(qcf.QCDate(d.isoformat()))"
   ],
   "outputs": [],
   "execution_count": 39
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Este procedimiento puede encapsularse fácilmente en una función, de hecho, la agregaremos al módulo `aux_functions` para seguir utilizándola más adelante."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T16:42:38.558483Z",
     "iopub.status.busy": "2024-07-08T16:42:38.557895Z",
     "iopub.status.idle": "2024-07-08T16:42:38.568700Z",
     "shell.execute_reply": "2024-07-08T16:42:38.567980Z",
     "shell.execute_reply.started": "2024-07-08T16:42:38.558411Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:28.791060Z",
     "start_time": "2025-06-06T11:21:28.787350Z"
    }
   },
   "source": [
    "def get_business_calendar(which_holidays: str, years: range) -> qcf.BusinessCalendar:\n",
    "    py_cal = hol.country_holidays(which_holidays, years=years)\n",
    "    yrs = [y for y in years]\n",
    "    qcf_cal = qcf.BusinessCalendar(qcf.QCDate(1, 1, yrs[0]), yrs[-1] - yrs[0])\n",
    "    for day in py_cal.keys():\n",
    "        qcf_cal.add_holiday(qcf.QCDate(day.isoformat()))\n",
    "    return qcf_cal"
   ],
   "outputs": [],
   "execution_count": 40
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Ejemplo:"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T16:42:39.648640Z",
     "iopub.status.busy": "2024-07-08T16:42:39.647916Z",
     "iopub.status.idle": "2024-07-08T16:42:39.663356Z",
     "shell.execute_reply": "2024-07-08T16:42:39.662504Z",
     "shell.execute_reply.started": "2024-07-08T16:42:39.648611Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:28.828315Z",
     "start_time": "2025-06-06T11:21:28.819366Z"
    }
   },
   "source": [
    "ny = get_business_calendar('US', range(2024, 2045))"
   ],
   "outputs": [],
   "execution_count": 41
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T16:42:40.139354Z",
     "iopub.status.busy": "2024-07-08T16:42:40.139047Z",
     "iopub.status.idle": "2024-07-08T16:42:40.147521Z",
     "shell.execute_reply": "2024-07-08T16:42:40.146734Z",
     "shell.execute_reply.started": "2024-07-08T16:42:40.139329Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:28.857220Z",
     "start_time": "2025-06-06T11:21:28.850901Z"
    }
   },
   "source": [
    "for i, d in enumerate(ny.get_holidays()):\n",
    "    if i < 10:\n",
    "        print(d)"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2024-01-01\n",
      "2024-01-15\n",
      "2024-02-19\n",
      "2024-05-27\n",
      "2024-06-19\n",
      "2024-07-04\n",
      "2024-09-02\n",
      "2024-10-14\n",
      "2024-11-11\n",
      "2024-11-28\n"
     ]
    }
   ],
   "execution_count": 42
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "heading_collapsed": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "## Fracciones de Año"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Las fracciones de año corresponden a las distintas formas de medir un intervalo de tiempo entre dos fechas que comúnmente se utiliza en los productos de tasa de interés."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "En `qcfinancial` están definidas las más utilizadas."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T16:42:46.266592Z",
     "iopub.status.busy": "2024-07-08T16:42:46.265903Z",
     "iopub.status.idle": "2024-07-08T16:42:46.275243Z",
     "shell.execute_reply": "2024-07-08T16:42:46.274468Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.266564Z"
    },
    "hidden": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:28.904630Z",
     "start_time": "2025-06-06T11:21:28.900605Z"
    }
   },
   "source": [
    "yfs = [\n",
    "    act360 := qcf.QCAct360(),\n",
    "    act365 := qcf.QCAct365(),\n",
    "    act30 := qcf.QCAct30(),\n",
    "    t30360 := qcf.QC30360(),\n",
    "    t3030 := qcf.QC3030(),\n",
    "    \n",
    "    # Corresponde a depósitos a plazo en CLP\n",
    "    act30 := qcf.QCAct30(),\n",
    "\n",
    "    # La utilizan los bonos del tesoro americano\n",
    "    actact := qcf.QCActAct(),\n",
    "]"
   ],
   "outputs": [],
   "execution_count": 43
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Métodos `yf` y `count_days`"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "El método `yf`, que retorna el valor de la fracción de año, está sobrecargado, se puede calcular usando como argumentos un número de días o un par de fechas (`QCDate`)."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T16:42:46.277165Z",
     "iopub.status.busy": "2024-07-08T16:42:46.276913Z",
     "iopub.status.idle": "2024-07-08T16:42:46.283630Z",
     "shell.execute_reply": "2024-07-08T16:42:46.283033Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.277142Z"
    },
    "hidden": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:28.956389Z",
     "start_time": "2025-06-06T11:21:28.951146Z"
    }
   },
   "source": [
    "print(f\"\\nfecha1: {fecha1} y fecha3: {fecha3}\")\n",
    "print(\"---------------------------------------\\n\")\n",
    "for yf in yfs:\n",
    "    print(type(yf))\n",
    "    print(f\"yf(30): {yf.yf(30):.6f}\")\n",
    "    print(f\"yf.yf(fecha1, fecha3): {yf.yf(fecha1, fecha3):.6f}\")\n",
    "    print(f\"yf.yf.count_days(fecha1, fecha3): {yf.count_days(fecha1, fecha3):.0f}\")\n",
    "    print()"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "fecha1: 2024-10-17 y fecha3: 2024-11-16\n",
      "---------------------------------------\n",
      "\n",
      "<class 'qcfinancial.QCAct360'>\n",
      "yf(30): 0.083333\n",
      "yf.yf(fecha1, fecha3): 0.083333\n",
      "yf.yf.count_days(fecha1, fecha3): 30\n",
      "\n",
      "<class 'qcfinancial.QCAct365'>\n",
      "yf(30): 0.082192\n",
      "yf.yf(fecha1, fecha3): 0.082192\n",
      "yf.yf.count_days(fecha1, fecha3): 30\n",
      "\n",
      "<class 'qcfinancial.QCAct30'>\n",
      "yf(30): 1.000000\n",
      "yf.yf(fecha1, fecha3): 1.000000\n",
      "yf.yf.count_days(fecha1, fecha3): 30\n",
      "\n",
      "<class 'qcfinancial.QC30360'>\n",
      "yf(30): 0.083333\n",
      "yf.yf(fecha1, fecha3): 0.080556\n",
      "yf.yf.count_days(fecha1, fecha3): 29\n",
      "\n",
      "<class 'qcfinancial.QC3030'>\n",
      "yf(30): 1.000000\n",
      "yf.yf(fecha1, fecha3): 0.966667\n",
      "yf.yf.count_days(fecha1, fecha3): 29\n",
      "\n",
      "<class 'qcfinancial.QCAct30'>\n",
      "yf(30): 1.000000\n",
      "yf.yf(fecha1, fecha3): 1.000000\n",
      "yf.yf.count_days(fecha1, fecha3): 30\n",
      "\n",
      "<class 'qcfinancial.QCActAct'>\n",
      "yf(30): 0.082192\n",
      "yf.yf(fecha1, fecha3): 0.082192\n",
      "yf.yf.count_days(fecha1, fecha3): 30\n",
      "\n"
     ]
    }
   ],
   "execution_count": 44
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "heading_collapsed": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "## Funciones y Factores de Capitalización"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Las funciones de capitalización representan las distintas formas en que se puede usar el valor de una tasa de interés para calcular o traer a valor presente un flujo de caja futuro. Al resultado de la función de capitalización lo llamamos *factor de capitalización*."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Están disponibles los siguientes 3 tipos de funciones (donde $yf$ es la fracción de año asociada a la tasa de valor $r$):\n",
    "\n",
    "- QCLinearWf:     $\\rightarrow 1 + r \\cdot yf$\n",
    "\n",
    "- QCCompoundWf:    $\\rightarrow \\left(1 + r \\right)^{yf}$\n",
    "\n",
    "- QCContinousWf:  $\\rightarrow exp(r \\cdot yf)$"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T16:42:46.284871Z",
     "iopub.status.busy": "2024-07-08T16:42:46.284594Z",
     "iopub.status.idle": "2024-07-08T16:42:46.288685Z",
     "shell.execute_reply": "2024-07-08T16:42:46.287969Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.284852Z"
    },
    "hidden": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:28.993631Z",
     "start_time": "2025-06-06T11:21:28.990893Z"
    }
   },
   "source": [
    "wfs = [\n",
    "    lin_wf:=qcf.QCLinearWf(),\n",
    "    com_wf:=qcf.QCCompoundWf(),\n",
    "    exp_wf:=qcf.QCContinousWf(),\n",
    "]"
   ],
   "outputs": [],
   "execution_count": 45
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Método `wf`"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Este método permite calcular el factor de capitalización a partir del valor de una tasa y el valor de una fracción de año."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T16:42:46.291016Z",
     "iopub.status.busy": "2024-07-08T16:42:46.290738Z",
     "iopub.status.idle": "2024-07-08T16:42:46.295963Z",
     "shell.execute_reply": "2024-07-08T16:42:46.295112Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.290994Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:29.039526Z",
     "start_time": "2025-06-06T11:21:29.033078Z"
    }
   },
   "source": [
    "r = .1   # Valor de la tasa\n",
    "yf = .5  # Fracción de año\n",
    "\n",
    "for wf in wfs:\n",
    "    print(f\"Función: {wf}. Factor: {wf.wf(r, yf):6f}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Función: Lin. Factor: 1.050000\n",
      "Función: Com. Factor: 1.048809\n",
      "Función: Exp. Factor: 1.051271\n"
     ]
    }
   ],
   "execution_count": 46
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Método `rate`"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Dada una función de capitalización, permite obtener la tasa de interés correspondiente a un factor de capitalización y fracción de año."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "En este caso el factor de capitalización es 1.1, la fracción de año es 1.0 y la función de capitalización es Linear."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T16:42:46.297068Z",
     "iopub.status.busy": "2024-07-08T16:42:46.296723Z",
     "iopub.status.idle": "2024-07-08T16:42:46.301946Z",
     "shell.execute_reply": "2024-07-08T16:42:46.301097Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.297045Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:29.081272Z",
     "start_time": "2025-06-06T11:21:29.076640Z"
    }
   },
   "source": [
    "print(f\"Tasa equivalente: {wfs[0].rate(1.1, 1.0):.4%}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Tasa equivalente: 10.0000%\n"
     ]
    }
   ],
   "execution_count": 47
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "## Tasas de Interés"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Utilizando un número real, una fracción de año y una función de capitalización, se puede dar de alta (instanciar) un objeto de tipo `QCInterestRate` que representa una tasa de interés (ver por ejemplo el video [Convenciones de Tasas](https://youtu.be/AdCMPKBFwgg?si=8v4wT1WER_poqEBg))."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T16:42:46.302996Z",
     "iopub.status.busy": "2024-07-08T16:42:46.302693Z",
     "iopub.status.idle": "2024-07-08T16:42:46.307293Z",
     "shell.execute_reply": "2024-07-08T16:42:46.306412Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.302975Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:29.133316Z",
     "start_time": "2025-06-06T11:21:29.128954Z"
    }
   },
   "source": [
    "r0 = 0.1\n",
    "tasas = [\n",
    "    tasa_lin_act360 := qcf.QCInterestRate(0.1, act360, lin_wf),\n",
    "    tasa_com_act365 := qcf.QCInterestRate(0.1, act365, com_wf),\n",
    "    tasa_exp_act365 := qcf.QCInterestRate(0.1, act365, exp_wf),\n",
    "]"
   ],
   "outputs": [],
   "execution_count": 48
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Métodos `get_value` y `set_value`"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Permiten obtener y definir el valor de la tasa de interés."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T16:42:46.308653Z",
     "iopub.status.busy": "2024-07-08T16:42:46.308354Z",
     "iopub.status.idle": "2024-07-08T16:42:46.314396Z",
     "shell.execute_reply": "2024-07-08T16:42:46.313186Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.308632Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:29.181151Z",
     "start_time": "2025-06-06T11:21:29.174019Z"
    }
   },
   "source": [
    "for tasa in tasas:\n",
    "    print(f\"Descripción: {tasa}\") # Está definido el método __str__\n",
    "    \n",
    "    # Se obtiene el valor de la tasa utilizando get_value\n",
    "    print(\"Obtener valor:\", tasa.get_value())\n",
    "    \n",
    "    # Se utiliza set_value para cambiar el valor de la tasa\n",
    "    r1 = 0.12\n",
    "    tasa.set_value(r1)\n",
    "    print(\"Obtener nuevo valor:\", tasa.get_value())\n",
    "    print()"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Descripción: 0.100000 Act360 Lin\n",
      "Obtener valor: 0.1\n",
      "Obtener nuevo valor: 0.12\n",
      "\n",
      "Descripción: 0.100000 Act365 Com\n",
      "Obtener valor: 0.1\n",
      "Obtener nuevo valor: 0.12\n",
      "\n",
      "Descripción: 0.100000 Act365 Exp\n",
      "Obtener valor: 0.1\n",
      "Obtener nuevo valor: 0.12\n",
      "\n"
     ]
    }
   ],
   "execution_count": 49
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Métodos `wf` y `dwf`"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Tanto `wf` como `dwf`son métodos sobrecargados. El primero permite calcular el valor del factor de capitalización de la tasa de interés utilizando un número de días o un par de fechas, mientras que el segundo calcula la derivada del factor de capitalización respecto a la tasa de interés. \n",
    "\n",
    "¿Cómo se realiza el cálculo de la derivada? Veamos un ejemplo:"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Consideremos una tasa de interés cuya función de capitalización es $g$. De ese modo el factor de capitalización $wf$ para un valor de tasa $r$ y una fracción de año $yf$ está dado por:"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "$$wf = g\\left(r,yf\\right)$$"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-07T15:30:27.186265Z",
     "iopub.status.busy": "2024-07-07T15:30:27.185958Z",
     "iopub.status.idle": "2024-07-07T15:30:27.193936Z",
     "shell.execute_reply": "2024-07-07T15:30:27.192638Z",
     "shell.execute_reply.started": "2024-07-07T15:30:27.186241Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "En muchas situaciones nos interesará saber como cambia el factor de capitalización cuando el valor $r$ de la tasa cambia. Cuando el cambio de valor, es pequeño, digamos un punto básico, resulta conveniente calcular el cambio de valor en $wf$, $\\Delta wf$ usando la derivada de la función $g$ respecto a $r$, más precisamente:"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "$$\\Delta wf = \\frac{dg\\left(r,yf\\right)}{dr}\\left(r_0,yf\\right)\\cdot\\delta$$"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-07T15:34:12.043104Z",
     "iopub.status.busy": "2024-07-07T15:34:12.042812Z",
     "iopub.status.idle": "2024-07-07T15:34:12.048522Z",
     "shell.execute_reply": "2024-07-07T15:34:12.047325Z",
     "shell.execute_reply.started": "2024-07-07T15:34:12.043078Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Donde $r_0$ es el valor inicial de la tasa y $\\delta$ es el cambio en su valor."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Tenemos que:"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "- Si $g=1+r\\cdot yf$ entonces $\\Delta wf = yf\\cdot\\delta$"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "- Si $g=\\left(1+r\\right)^{yf}$ entonces $\\Delta wf = yf\\cdot\\left(1+r_0\\right)^{yf-1}\\cdot\\delta$"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "- Si $g=exp\\left(r\\cdot yf\\right)$ entonces $\\Delta wf = yf\\cdot exp\\left(r_0\\cdot yf\\right)\\cdot\\delta$"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Calculemos `wf` y `dwf` usando un par de fechas."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T16:42:46.315488Z",
     "iopub.status.busy": "2024-07-08T16:42:46.315131Z",
     "iopub.status.idle": "2024-07-08T16:42:46.324466Z",
     "shell.execute_reply": "2024-07-08T16:42:46.323794Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.315468Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:24:17.015622Z",
     "start_time": "2025-06-06T11:24:17.009950Z"
    }
   },
   "source": [
    "for i, tasa in enumerate(tasas):\n",
    "    # Retorna el factor de capitalización entre las fechas\n",
    "    print(f\"wf(fecha1, fecha3): {tasa.wf(fecha1, fecha3):.8f}\")\n",
    "\n",
    "    # Retorna la derivada del factor de capitalización respecto al valor de la tasa entre las fechas\n",
    "    print(f\"dwf(fecha1, fecha3): {tasa.dwf(fecha1, fecha3):.8f}\")\n",
    "\n",
    "    # Para verificar se calcula \"a mano\" la derivada\n",
    "    match i:\n",
    "        case 0:\n",
    "            print(f\"Check: {tasa.yf(fecha1, fecha3):.8f}\")\n",
    "        case 1:\n",
    "            yf_ = tasa.yf(fecha1, fecha3)\n",
    "            print(f\"Check: {tasa.yf(fecha1, fecha3) * (1 + tasa.get_value())**(yf_ - 1):.8f}\")\n",
    "        case 2:\n",
    "            print(f\"Check: {tasa.yf(fecha1, fecha3) * tasa.wf(fecha1, fecha3):.8f}\")\n",
    "    \n",
    "    print()"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "wf(fecha1, fecha3): 1.01000000\n",
      "dwf(fecha1, fecha3): 0.08333333\n",
      "Check: 0.08333333\n",
      "\n",
      "wf(fecha1, fecha3): 1.00935820\n",
      "dwf(fecha1, fecha3): 0.07407228\n",
      "Check: 0.07407228\n",
      "\n",
      "wf(fecha1, fecha3): 1.00991181\n",
      "dwf(fecha1, fecha3): 0.08300645\n",
      "Check: 0.08300645\n",
      "\n"
     ]
    }
   ],
   "execution_count": 78
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Veamos ahora la sobrecarga y utilicemos un número de días."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T16:42:46.325539Z",
     "iopub.status.busy": "2024-07-08T16:42:46.325362Z",
     "iopub.status.idle": "2024-07-08T16:42:46.331435Z",
     "shell.execute_reply": "2024-07-08T16:42:46.330829Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.325522Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:24:41.906353Z",
     "start_time": "2025-06-06T11:24:41.900765Z"
    }
   },
   "source": [
    "dias = 400\n",
    "for i, tasa in enumerate(tasas):\n",
    "    # Retorna el factor de capitalización entre las fechas\n",
    "    print(f\"wf(dias): {tasa.wf(dias):.8F}\")\n",
    "\n",
    "    # Retorna la derivada del factor de capitalización respecto al valor de la tasa entre las fechas\n",
    "    print(f\"dwf(dias): {tasa.dwf(dias):.8f}\")\n",
    "\n",
    "    # Para verificar se calcula \"a mano\" la derivada\n",
    "    match i:\n",
    "        case 0:\n",
    "            print(f\"Check: {dias / 360:.8f}\")\n",
    "        case 1:\n",
    "            yf_ = dias / 365\n",
    "            print(f\"Check: {yf_ * (1 + tasa.get_value())**(yf_ - 1):.8f}\")\n",
    "        case 2:\n",
    "            print(f\"Check: {dias / 365 * tasa.wf(dias):.8f}\")\n",
    "    \n",
    "    print()"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "wf(dias): 1.13333333\n",
      "dwf(dias): 1.11111111\n",
      "Check: 1.11111111\n",
      "\n",
      "wf(dias): 1.13223756\n",
      "dwf(dias): 1.10786454\n",
      "Check: 1.10786454\n",
      "\n",
      "wf(dias): 1.14054572\n",
      "dwf(dias): 1.24991312\n",
      "Check: 1.24991312\n",
      "\n"
     ]
    }
   ],
   "execution_count": 79
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Método `get_rate_from_wf`"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Este método permite calcular la tasa de interés correspondiente a un dado factor de capitalización, utilizando la función de capitalización y la fracción de año de la tasa. El intervalo de tiempo de la tasa se puede especificar con un par de fechas o con un número de días."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Veamos un ejemplo:"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T16:42:46.336319Z",
     "iopub.status.busy": "2024-07-08T16:42:46.336078Z",
     "iopub.status.idle": "2024-07-08T16:42:46.341956Z",
     "shell.execute_reply": "2024-07-08T16:42:46.341191Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.336300Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:29.339811Z",
     "start_time": "2025-06-06T11:21:29.336152Z"
    }
   },
   "source": [
    "factor = 1.0025\n",
    "dias = 31\n",
    "for tasa in tasas:\n",
    "    aux = f\"{tasa}\"[-10:]\n",
    "    print(f\"Tasa: {aux}\")\n",
    "    print(f\"get_rate_from_wf(factor, fecha1, fecha3): {tasa.get_rate_from_wf(factor, fecha1, fecha3):.4%}\")\n",
    "    print(f\"get_rate_from_wf(factor, dias): {tasa.get_rate_from_wf(factor, dias):.4%}\\n\")\n"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Tasa: Act360 Lin\n",
      "get_rate_from_wf(factor, fecha1, fecha3): 3.0000%\n",
      "get_rate_from_wf(factor, dias): 2.9032%\n",
      "\n",
      "Tasa: Act365 Com\n",
      "get_rate_from_wf(factor, fecha1, fecha3): 3.0845%\n",
      "get_rate_from_wf(factor, dias): 2.9835%\n",
      "\n",
      "Tasa: Act365 Exp\n",
      "get_rate_from_wf(factor, fecha1, fecha3): 3.0379%\n",
      "get_rate_from_wf(factor, dias): 2.9399%\n",
      "\n"
     ]
    }
   ],
   "execution_count": 52
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "## Tenor"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Es una clase que representa el concepto de plazo estructurado o tenor (1D, 1M, 1Y ...)."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Ejemplos"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T16:42:46.342898Z",
     "iopub.status.busy": "2024-07-08T16:42:46.342645Z",
     "iopub.status.idle": "2024-07-08T16:42:46.349275Z",
     "shell.execute_reply": "2024-07-08T16:42:46.348303Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.342877Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:29.420948Z",
     "start_time": "2025-06-06T11:21:29.417511Z"
    }
   },
   "source": [
    "tenors = [\n",
    "    _1d := qcf.Tenor(\"1d\"),\n",
    "    _1m := qcf.Tenor(\"1M\"),\n",
    "    _1y := qcf.Tenor(\"1y\"),\n",
    "    _1d_1m_1y := qcf.Tenor(\"1D1M1Y\"),\n",
    "\n",
    "    # Notar que, en este caso, el constructor es capaz de eliminar\n",
    "    # los espacios y la substr nyse\n",
    "    _2y_3m := qcf.Tenor(\"2y nyse 3m\"),  \n",
    "]"
   ],
   "outputs": [],
   "execution_count": 53
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Métodos `get_string`, `get_days`, `get_months` y `get_years`"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T16:42:46.350439Z",
     "iopub.status.busy": "2024-07-08T16:42:46.350033Z",
     "iopub.status.idle": "2024-07-08T16:42:46.356017Z",
     "shell.execute_reply": "2024-07-08T16:42:46.355372Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.350411Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:29.461146Z",
     "start_time": "2025-06-06T11:21:29.449932Z"
    }
   },
   "source": [
    "for tenor in tenors:\n",
    "    print(f\"string: {tenor.get_string()}\")\n",
    "    print(f\"dias: {tenor.get_days()}\")\n",
    "    print(f\"meses: {tenor.get_months()}\")\n",
    "    print(f\"años: {tenor.get_years()}\\n\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "string: 1D\n",
      "dias: 1\n",
      "meses: 0\n",
      "años: 0\n",
      "\n",
      "string: 1M\n",
      "dias: 0\n",
      "meses: 1\n",
      "años: 0\n",
      "\n",
      "string: 1Y\n",
      "dias: 0\n",
      "meses: 0\n",
      "años: 1\n",
      "\n",
      "string: 1Y1M1D\n",
      "dias: 1\n",
      "meses: 1\n",
      "años: 1\n",
      "\n",
      "string: 2Y3M\n",
      "dias: 0\n",
      "meses: 3\n",
      "años: 2\n",
      "\n"
     ]
    }
   ],
   "execution_count": 54
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Método `set_tenor`"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T16:42:46.356927Z",
     "iopub.status.busy": "2024-07-08T16:42:46.356748Z",
     "iopub.status.idle": "2024-07-08T16:42:46.360908Z",
     "shell.execute_reply": "2024-07-08T16:42:46.360055Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.356908Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:29.533584Z",
     "start_time": "2025-06-06T11:21:29.528025Z"
    }
   },
   "source": [
    "for i, tenor in enumerate(tenors):\n",
    "    tenor.set_tenor(f\"{i}d{i}m{i}y\")\n",
    "    print(f\"string: {tenor.get_string()}\\n\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "string: 0D\n",
      "\n",
      "string: 1Y1M1D\n",
      "\n",
      "string: 2Y2M2D\n",
      "\n",
      "string: 3Y3M3D\n",
      "\n",
      "string: 4Y4M4D\n",
      "\n"
     ]
    }
   ],
   "execution_count": 55
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "heading_collapsed": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "## FX Rate"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Es una clase que representa el concepto de tipo de cambio entre dos monedas. Para dar de alta un FXRate se requiere:"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": ""
    },
    "tags": []
   },
   "source": [
    "- QCCurrency: la moneda fuerte del par."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": ""
    },
    "tags": []
   },
   "source": [
    "- QCCurrency: la moneda débl del par."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Ejemplo: USDCLP"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T16:42:46.362487Z",
     "iopub.status.busy": "2024-07-08T16:42:46.362211Z",
     "iopub.status.idle": "2024-07-08T16:42:46.366481Z",
     "shell.execute_reply": "2024-07-08T16:42:46.365872Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.362465Z"
    },
    "hidden": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:29.608603Z",
     "start_time": "2025-06-06T11:21:29.605251Z"
    }
   },
   "source": [
    "usdclp = qcf.FXRate(usd, clp)"
   ],
   "outputs": [],
   "execution_count": 56
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Utilizando el método `get_code` se puede obtener el código del par según la convención usual."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T16:42:46.368810Z",
     "iopub.status.busy": "2024-07-08T16:42:46.368561Z",
     "iopub.status.idle": "2024-07-08T16:42:46.372040Z",
     "shell.execute_reply": "2024-07-08T16:42:46.371425Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.368791Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:29.644170Z",
     "start_time": "2025-06-06T11:21:29.640311Z"
    }
   },
   "source": [
    "print(f\"Código: {usdclp.get_code()}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Código: USDCLP\n"
     ]
    }
   ],
   "execution_count": 57
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "## FX Rate Index"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Esta clase representa un índice de tipo de cambio, por ejemplo, el dólar observado que publica el Banco Central de Chile."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Para dar de alta un FXRateIndex se requiere:\n",
    "\n",
    "- `FXRate`: el FXRate correspondiente.\n",
    "- `str`: nombre del índice\n",
    "- `Tenor`: la regla de fixing, es 1D como el USD Observado o es 0D como un índice de cierre de día.\n",
    "- `Tenor`: la regla para la valuta. Es 1D como el USDCLP o 2D como el EURUSD.\n",
    "- `BusinessCalendar`: el calendario adecuado para aplicar las reglas de fixing y valuta."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Ejemplo"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-07-08T16:42:46.373206Z",
     "iopub.status.busy": "2024-07-08T16:42:46.373005Z",
     "iopub.status.idle": "2024-07-08T16:42:46.749726Z",
     "shell.execute_reply": "2024-07-08T16:42:46.747531Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.373186Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:29.685380Z",
     "start_time": "2025-06-06T11:21:29.679883Z"
    }
   },
   "source": [
    "_1d.set_tenor(\"1d\")\n",
    "usdclp_obs = qcf.FXRateIndex(usdclp, \"USDOBS\", _1d, _1d, scl)"
   ],
   "outputs": [],
   "execution_count": 58
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Métodos `fixing_date` y `value_date`"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "El método `fixing_date` retorna la fecha de fixing del índice dada la fecha de publicación. Por su parte, `value_date` retorna la fecha de la valuta dada la fecha de publicación."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.status.busy": "2024-07-08T16:42:46.750278Z",
     "iopub.status.idle": "2024-07-08T16:42:46.750547Z",
     "shell.execute_reply": "2024-07-08T16:42:46.750417Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.750405Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:29.741014Z",
     "start_time": "2025-06-06T11:21:29.737410Z"
    }
   },
   "source": [
    "print(f\"Fecha de publicación: {fecha1.week_day()}, {fecha1}\")\n",
    "print(f\"Fecha de fixing: {usdclp_obs.fixing_date(fecha1)}\")\n",
    "print(f\"Fecha de valuta: {usdclp_obs.value_date(fecha1)}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Fecha de publicación: WeekDay.THU, 2024-10-17\n",
      "Fecha de fixing: 2024-10-16\n",
      "Fecha de valuta: 2024-10-17\n"
     ]
    }
   ],
   "execution_count": 59
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Notar que la fecha de fixing se calcula aplicando la regla de fixing a la fecha de publicación, mientras que la fecha de valuta se calcula aplicando la regla de valuta a la fecha de fixing."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Método `convert`"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "El método `convert` permite pasar rápidamente de una moneda a la otra (de las que forman el par del índice) usando un valor para el índice."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Veamos un ejemplo:"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.status.busy": "2024-07-08T16:42:46.751576Z",
     "iopub.status.idle": "2024-07-08T16:42:46.751860Z",
     "shell.execute_reply": "2024-07-08T16:42:46.751734Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.751722Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:29.795644Z",
     "start_time": "2025-06-06T11:21:29.791268Z"
    }
   },
   "source": [
    "monto_usd = 1_000_000\n",
    "monto_clp = 900_000_000\n",
    "valor_usdclp_obs = 900.00\n",
    "\n",
    "result = usdclp_obs.convert(monto_usd, qcf.QCUSD(), valor_usdclp_obs)\n",
    "print(f\"Monto en CLP es: {result:,.0f}\")\n",
    "\n",
    "result = usdclp_obs.convert(monto_clp, qcf.QCCLP(), valor_usdclp_obs)\n",
    "print(f\"Monto en USD es: {result:,.0f}\")"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Monto en CLP es: 900,000,000\n",
      "Monto en USD es: 1,000,000\n"
     ]
    }
   ],
   "execution_count": 60
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-05-26T14:21:20.952930Z",
     "iopub.status.busy": "2024-05-26T14:21:20.952572Z",
     "iopub.status.idle": "2024-05-26T14:21:20.958741Z",
     "shell.execute_reply": "2024-05-26T14:21:20.957842Z",
     "shell.execute_reply.started": "2024-05-26T14:21:20.952899Z"
    },
    "slideshow": {
     "slide_type": ""
    },
    "tags": []
   },
   "source": [
    "Esta función es cómoda porque evita tener que controlar en el propio código si la divisa del monto a convertir es la fuerte o la débil del par."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "## QCCurrencyConverter"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Este es un objeto que permite realizar conversiones de una moneda a otra con un poco más de generalidad que en el caso anterior."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.status.busy": "2024-07-08T16:42:46.752715Z",
     "iopub.status.idle": "2024-07-08T16:42:46.752924Z",
     "shell.execute_reply": "2024-07-08T16:42:46.752817Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.752807Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:29.854150Z",
     "start_time": "2025-06-06T11:21:29.850165Z"
    }
   },
   "source": [
    "ccy_converter = qcf.QCCurrencyConverter()"
   ],
   "outputs": [],
   "execution_count": 61
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Método `convert`"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "El método `convert` se puede utilizar con dos conjuntos distintos de argumentos:\n",
    "\n",
    "- `float`: que representa el monto en una divisa a convertir,\n",
    "- `QCCurrency`: que representa la divisa del monto anterior\n",
    "- `float`: que representa el valor del tipo de cambio a utilizar en la convención de mercado del par\n",
    "- `FXRateIndex`: que representa el par de monedas entre las cuales se realiza la conversión"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Por ejemplo:"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.status.busy": "2024-07-08T16:42:46.754785Z",
     "iopub.status.idle": "2024-07-08T16:42:46.755252Z",
     "shell.execute_reply": "2024-07-08T16:42:46.755083Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.755071Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:29.912255Z",
     "start_time": "2025-06-06T11:21:29.907319Z"
    }
   },
   "source": [
    "print(f'Monto en CLP: {ccy_converter.convert(monto_usd, usd, 900, usdclp_obs):,.0f}')\n",
    "print(f'Monto en USD: {ccy_converter.convert(monto_clp, clp, 900, usdclp_obs):,.0f}')"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Monto en CLP: 900,000,000\n",
      "Monto en USD: 1,000,000\n"
     ]
    }
   ],
   "execution_count": 62
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Para el segundo método se introducen dos `enum` definidos en `QCCurrencyConverter`:"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "#### Enum para Monedas"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.status.busy": "2024-07-08T16:42:46.756112Z",
     "iopub.status.idle": "2024-07-08T16:42:46.756525Z",
     "shell.execute_reply": "2024-07-08T16:42:46.756360Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.756335Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:29.977522Z",
     "start_time": "2025-06-06T11:21:29.969857Z"
    }
   },
   "source": [
    "qcf.QCCurrencyEnum.CLP"
   ],
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<QCCurrencyEnum.CLP: 6>"
      ]
     },
     "execution_count": 63,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "execution_count": 63
  },
  {
   "cell_type": "code",
   "metadata": {
    "collapsed": false,
    "editable": true,
    "execution": {
     "iopub.status.busy": "2024-07-08T16:42:46.757601Z",
     "iopub.status.idle": "2024-07-08T16:42:46.758065Z",
     "shell.execute_reply": "2024-07-08T16:42:46.757892Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.757869Z"
    },
    "jupyter": {
     "outputs_hidden": false
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:30.058027Z",
     "start_time": "2025-06-06T11:21:30.053048Z"
    }
   },
   "source": [
    "qcf.QCCurrencyEnum.USD"
   ],
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<QCCurrencyEnum.USD: 18>"
      ]
     },
     "execution_count": 64,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "execution_count": 64
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "#### Enum para FXRates"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.status.busy": "2024-07-08T16:42:46.759300Z",
     "iopub.status.idle": "2024-07-08T16:42:46.759733Z",
     "shell.execute_reply": "2024-07-08T16:42:46.759615Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.759604Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:30.124957Z",
     "start_time": "2025-06-06T11:21:30.119947Z"
    }
   },
   "source": [
    "qcf.QCFxRateEnum.USDCLP"
   ],
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<QCFxRateEnum.USDCLP: 15>"
      ]
     },
     "execution_count": 65,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "execution_count": 65
  },
  {
   "cell_type": "code",
   "metadata": {
    "collapsed": false,
    "editable": true,
    "execution": {
     "iopub.status.busy": "2024-07-08T16:42:46.760806Z",
     "iopub.status.idle": "2024-07-08T16:42:46.761230Z",
     "shell.execute_reply": "2024-07-08T16:42:46.761028Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.760998Z"
    },
    "jupyter": {
     "outputs_hidden": false
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:30.180408Z",
     "start_time": "2025-06-06T11:21:30.175647Z"
    }
   },
   "source": [
    "qcf.QCFxRateEnum.EURUSD"
   ],
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<QCFxRateEnum.EURUSD: 31>"
      ]
     },
     "execution_count": 66,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "execution_count": 66
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Con estos `enum` el segundo conjunto de argumentos para el método `convert` es:\n",
    "\n",
    "- float: que representa el monto en una divisa a convertir,\n",
    "- QCCurrencyEnum: que representa la divisa del monto anterior\n",
    "- float: que representa el valor del tipo de cambio a utilizar en la convención de mercado del par\n",
    "- QCFxRateEnum: que representa el par de monedas entre las cuales se realiza la conversión"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Por ejemplo:"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.status.busy": "2024-07-08T16:42:46.762390Z",
     "iopub.status.idle": "2024-07-08T16:42:46.762716Z",
     "shell.execute_reply": "2024-07-08T16:42:46.762592Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.762579Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:30.253584Z",
     "start_time": "2025-06-06T11:21:30.247136Z"
    }
   },
   "source": [
    "print(f'Monto en USD: {ccy_converter.convert(monto_clp, qcf.QCCurrencyEnum.CLP, 900, qcf.QCFxRateEnum.USDCLP):,.0f}')\n",
    "print(f'Monto en CLP: {ccy_converter.convert(monto_usd, qcf.QCCurrencyEnum.USD, 900, qcf.QCFxRateEnum.USDCLP):,.0f}')"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Monto en USD: 1,000,000\n",
      "Monto en CLP: 900,000,000\n"
     ]
    }
   ],
   "execution_count": 67
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.execute_input": "2024-05-26T15:12:28.240823Z",
     "iopub.status.busy": "2024-05-26T15:12:28.240443Z",
     "iopub.status.idle": "2024-05-26T15:12:28.281519Z",
     "shell.execute_reply": "2024-05-26T15:12:28.280077Z",
     "shell.execute_reply.started": "2024-05-26T15:12:28.240792Z"
    },
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Las divisas disponibles en `QCCurrencyEnum` son las mismas que en `QCCurrency`:"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.status.busy": "2024-07-08T16:42:46.763843Z",
     "iopub.status.idle": "2024-07-08T16:42:46.764260Z",
     "shell.execute_reply": "2024-07-08T16:42:46.764104Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.764090Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:30.306217Z",
     "start_time": "2025-06-06T11:21:30.301347Z"
    }
   },
   "source": [
    "qcf.QCCurrencyEnum.AUD"
   ],
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<QCCurrencyEnum.AUD: 0>"
      ]
     },
     "execution_count": 68,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "execution_count": 68
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.status.busy": "2024-07-08T16:42:46.765385Z",
     "iopub.status.idle": "2024-07-08T16:42:46.765844Z",
     "shell.execute_reply": "2024-07-08T16:42:46.765688Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.765658Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:30.375935Z",
     "start_time": "2025-06-06T11:21:30.370908Z"
    }
   },
   "source": [
    "qcf.QCCurrencyEnum.BRL"
   ],
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<QCCurrencyEnum.BRL: 1>"
      ]
     },
     "execution_count": 69,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "execution_count": 69
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.status.busy": "2024-07-08T16:42:46.767112Z",
     "iopub.status.idle": "2024-07-08T16:42:46.767565Z",
     "shell.execute_reply": "2024-07-08T16:42:46.767391Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.767377Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:30.459024Z",
     "start_time": "2025-06-06T11:21:30.451763Z"
    }
   },
   "source": [
    "qcf.QCCurrencyEnum.PEN"
   ],
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<QCCurrencyEnum.PEN: 16>"
      ]
     },
     "execution_count": 70,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "execution_count": 70
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "Los pares de divisas en `QCFxRateEnum` son los pares de las divisas versus el USD (en su convención de mercado) y las divisas versus CLP, que aunque no son pares líquidos, son útiles cuando se quiere expresar montos en cualquier divisa en CLP."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.status.busy": "2024-07-08T16:42:46.769111Z",
     "iopub.status.idle": "2024-07-08T16:42:46.769570Z",
     "shell.execute_reply": "2024-07-08T16:42:46.769417Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.769402Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:30.532019Z",
     "start_time": "2025-06-06T11:21:30.526235Z"
    }
   },
   "source": [
    "qcf.QCFxRateEnum.USDCLP"
   ],
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<QCFxRateEnum.USDCLP: 15>"
      ]
     },
     "execution_count": 71,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "execution_count": 71
  },
  {
   "cell_type": "code",
   "metadata": {
    "collapsed": false,
    "editable": true,
    "execution": {
     "iopub.status.busy": "2024-07-08T16:42:46.770952Z",
     "iopub.status.idle": "2024-07-08T16:42:46.771852Z",
     "shell.execute_reply": "2024-07-08T16:42:46.771646Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.771615Z"
    },
    "jupyter": {
     "outputs_hidden": false
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:30.607796Z",
     "start_time": "2025-06-06T11:21:30.602420Z"
    }
   },
   "source": [
    "qcf.QCFxRateEnum.EURUSD"
   ],
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<QCFxRateEnum.EURUSD: 31>"
      ]
     },
     "execution_count": 72,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "execution_count": 72
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.status.busy": "2024-07-08T16:42:46.772792Z",
     "iopub.status.idle": "2024-07-08T16:42:46.773353Z",
     "shell.execute_reply": "2024-07-08T16:42:46.773145Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.773133Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:30.682679Z",
     "start_time": "2025-06-06T11:21:30.676975Z"
    }
   },
   "source": [
    "qcf.QCFxRateEnum.EURCLP"
   ],
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<QCFxRateEnum.EURCLP: 32>"
      ]
     },
     "execution_count": 73,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "execution_count": 73
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "## Time Series"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": []
   },
   "source": [
    "Este es un objeto que permite almacenar series de tiempo financieras y se utilizarán más adelante en el fixing y valorización de flujos de caja de tasa de interés. Su estructura interna es muy similar a la de un objeto `dict[datetime.date, float]` en Python, sólo se debe reemplazar la `key` del `dict` por un objeto de tipo `QCCDate`."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": "slide"
    },
    "tags": []
   },
   "source": [
    "### Ejemplo"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.status.busy": "2024-07-08T16:42:46.774939Z",
     "iopub.status.idle": "2024-07-08T16:42:46.775384Z",
     "shell.execute_reply": "2024-07-08T16:42:46.775269Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.775257Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:30.753007Z",
     "start_time": "2025-06-06T11:21:30.749614Z"
    }
   },
   "source": [
    "ts = qcf.time_series()\n",
    "ts[fecha1] = 10.0"
   ],
   "outputs": [],
   "execution_count": 74
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.status.busy": "2024-07-08T16:42:46.776605Z",
     "iopub.status.idle": "2024-07-08T16:42:46.777206Z",
     "shell.execute_reply": "2024-07-08T16:42:46.776963Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.776932Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:30.795491Z",
     "start_time": "2025-06-06T11:21:30.789538Z"
    }
   },
   "source": [
    "type(ts)"
   ],
   "outputs": [
    {
     "data": {
      "text/plain": [
       "qcfinancial.time_series"
      ]
     },
     "execution_count": 75,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "execution_count": 75
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.status.busy": "2024-07-08T16:42:46.779299Z",
     "iopub.status.idle": "2024-07-08T16:42:46.780232Z",
     "shell.execute_reply": "2024-07-08T16:42:46.779987Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.779939Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:30.845348Z",
     "start_time": "2025-06-06T11:21:30.840224Z"
    }
   },
   "source": [
    "ts[fecha1]"
   ],
   "outputs": [
    {
     "data": {
      "text/plain": [
       "10.0"
      ]
     },
     "execution_count": 76,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "execution_count": 76
  },
  {
   "cell_type": "code",
   "metadata": {
    "editable": true,
    "execution": {
     "iopub.status.busy": "2024-07-08T16:42:46.781986Z",
     "iopub.status.idle": "2024-07-08T16:42:46.782597Z",
     "shell.execute_reply": "2024-07-08T16:42:46.782425Z",
     "shell.execute_reply.started": "2024-07-08T16:42:46.782392Z"
    },
    "slideshow": {
     "slide_type": "fragment"
    },
    "tags": [],
    "ExecuteTime": {
     "end_time": "2025-06-06T11:21:30.920026Z",
     "start_time": "2025-06-06T11:21:30.913342Z"
    }
   },
   "source": [
    "for k, v in ts.items():\n",
    "    print(k, v)"
   ],
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2024-10-17 10.0\n"
     ]
    }
   ],
   "execution_count": 77
  }
 ],
 "metadata": {
  "hide_input": false,
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.5"
  },
  "toc": {
   "base_numbering": 1,
   "nav_menu": {},
   "number_sections": true,
   "sideBar": true,
   "skip_h1_title": true,
   "title_cell": "Table of Contents",
   "title_sidebar": "Contenido",
   "toc_cell": false,
   "toc_position": {
    "height": "675.455px",
    "left": "284px",
    "top": "282.284px",
    "width": "235px"
   },
   "toc_section_display": true,
   "toc_window_display": true
  },
  "varInspector": {
   "cols": {
    "lenName": 16,
    "lenType": 16,
    "lenVar": 40
   },
   "kernels_config": {
    "python": {
     "delete_cmd_postfix": "",
     "delete_cmd_prefix": "del ",
     "library": "var_list.py",
     "varRefreshCmd": "print(var_dic_list())"
    },
    "r": {
     "delete_cmd_postfix": ") ",
     "delete_cmd_prefix": "rm(",
     "library": "var_list.r",
     "varRefreshCmd": "cat(var_dic_list()) "
    }
   },
   "types_to_exclude": [
    "module",
    "function",
    "builtin_function_or_method",
    "instance",
    "_Feature"
   ],
   "window_display": false
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
