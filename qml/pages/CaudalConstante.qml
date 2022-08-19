import QtQuick 6
import QtQuick.Window 2.15
import QtQuick.Controls 6
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts

Item{
    
    Material.theme: Material.Dark
    Material.accent: Material.LightBlue

    property var list1:["Nivel Mínimo [m]:","Nivel Máximo [m]:","Caudal Objetivo [m³/s]:"]
    property var list2:["Nivel Mínimo [m]:","Nivel Máximo [m]:","Déficit Buscado [%]:"]
    property var list3:["Nivel Mínimo [m]:","Nivel Máximo Límite [m]:","Déficit Buscado [%]:","Paso de Cálculo:"]
    property var lista:[list1,list2,["Nivel Mínimo [m]:","Déficit Buscado [%]:"]]
    property var lista_input:[list1,list2,list3]

    property var cant_variables : [[1,1,1],[1,1,1],[1,1,1,1]]

    function change_values(index,value,text){

        var error = false
        var model_list = [list1,list2,list3][index]
        var pos = model_list.indexOf(text)
        var result_list = []
        cant_variables[index][pos] = value
        for(var i=0 ; i < cant_variables[index].length ; i++){
            var element = cant_variables[index][i]
            if(i != pos && element != 1){
                cant_variables[index][pos] = 1
                console.log(cant_variables)
                error = true
            }
        }
        if(error){
            repeater_error.itemAt(index).text = "Se pueden agregar elementos de una única variable"
        }else{
            repeater_error.itemAt(index).text = ""
            model_list.forEach(function(texto){
                if(texto == text){
                    for (var i = 0; i<value; i++){
                        result_list.push(text)
                    }
                }else{
                    result_list.push(texto)
                }
                })

            lista_input[index] = result_list
            repeater_input.model = lista_input
        }
        
        
    }
    property var text:if(btn_calculo_total.hovered){
                                "total"
                            }else if(btn_calculo_falla.hovered){
                                "falla"
                            }else if(btn_calculo_garantia.hovered){
                                "garantia"
                            }

    Rectangle {
        id: rectangle
        color: "#2c313c"
        anchors.fill: parent

        ScrollView{

            id: scroller_grid
            anchors.fill: parent
            clip : true

            Rectangle {
                id: rectangleTop
                //height: 69
                //color: "#495163"
                color: "#2c313c"
                radius: 10
                anchors.left: parent.left
                anchors.top: parent.top
                anchors.leftMargin: 20
                anchors.topMargin: 10

                default property alias data: grid.data
                implicitWidth: grid.implicitWidth
                implicitHeight: grid.implicitHeight


                
                GridLayout {
                    id:grid
                    anchors.fill: parent
                    columns:3
                    columnSpacing:50
                    
                    Repeater{
                        model:["CONSIGNA CAUDAL","CONSIGNA DÉFICIT","CURVA GARANTÍA"]
                        Rectangle{
                            color: Material.color(Material.Blue)
                            Layout.topMargin:20
                            Layout.fillHeight: true
                            Layout.fillWidth:true
                            Layout.preferredHeight :50
                            radius:10
                            implicitWidth: text.implicitWidth
                            implicitHeight: text.implicitHeight

                            Text{
                                id:text
                                text: modelData
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.horizontalCenter: parent.horizontalCenter
                                color:"#ffffff"
                                font.pointSize: 11
                            }
                        }
                    }
                    Repeater{
                        id: repeater_combobox
                        model:3

                        GridLayout{
                            id:control_parent
                            columns:3
                            ComboBox{
                                id:count
                                model:[1,2,3,4,5]
                                Layout.preferredWidth:70
                                Layout.leftMargin:20
                                delegate: ItemDelegate {
                                    width: parent.width
                                    contentItem: Text {
                                        text: modelData
                                        color: "#fff"
                                        font: parent.font
                                        elide: Text.ElideRight
                                        verticalAlignment: Text.AlignVCenter
                                    }
                                    background: Rectangle {
                                        //border.color: Material.color(Material.Blue)
                                        color:"#495163"
                                        
                                    }
                                }
                                
                            }
                            ComboBox{
                                model:lista[index]
                                Layout.preferredWidth:160
                                Layout.leftMargin:20
                                id: control
                                delegate: ItemDelegate {
                                    width: control.width
                                    contentItem: Text {
                                        text: modelData
                                        color: "#fff"
                                        font: control.font
                                        elide: Text.ElideRight
                                        verticalAlignment: Text.AlignVCenter
                                    }
                                    background: Rectangle {
                                        //border.color: Material.color(Material.Blue)
                                        color:"#495163"
                                    }
                                }
                            }
                            Button{
                                id:control_btn
                                Layout.leftMargin:20
                                text:"OK"
                                onClicked:{
                                    change_values(index,count.currentText,control.currentText)

                                }
                            }
                        }
                    }
                    Repeater{
                        id:repeater_input
                        model:lista_input
                        ScrollView{

                            id: scroller_grid
                            Layout.preferredHeight: 200
                            Layout.fillWidth: true
                            clip : true
                            

                            GridLayout {
                                columns: 1
                                rows:4
                                columnSpacing:10
                                anchors.horizontalCenter: parent.horizontalCenter


                                Repeater{
                                    id: repeater_calculo_total
                                    model:modelData
                                    GridLayout{
                                        columns:2
                                        columnSpacing:10
                                        Text{
                                            id:txt
                                            Layout.preferredWidth: 160
                                            Layout.leftMargin:40
                                            text: modelData
                                            font.pointSize: 11
                                            color: "#fff"
                                        }
                                        TextField{
                                            id:txt_field
                                            font.pointSize: 11
                                            Layout.leftMargin:5
                                            Layout.rightMargin:5
                                            Layout.preferredWidth: 100
                                            text: qsTr("")
                                            selectByMouse: true
                                
                                        }
                                    }
                                    
                                }
                                
                            }
                        }
                    }
                    Repeater{
                        id:repeater_error
                        model:3
                        Text{
                            text: qsTr("")
                            Layout.fillWidth: true
                            Layout.preferredWidth: 260
                            wrapMode:Text.Wrap
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                            color:"#f00"
                            font.pointSize: 11
                        }
                    }

                    Button{
                        id: btn_calculo_total
                        property bool isrunning:false
                        Layout.alignment:Qt.AlignHCenter
                        Layout.preferredWidth: 200
                        text: qsTr("Comenzar")
                        opacity:5
                        Material.background: Material.color(Material.Green,Material.ShadeA700)
                        Material.elevation: 6
                        onClicked:{

                            if (isrunning){
                                backend.stop_falla_cc()
                                Material.background = Material.color(Material.Green,Material.ShadeA700)
                                btn_calculo_total.text = "Comenzar"
                                btn_calculo_total.isrunning=false

                            }else{
                                conections.verification(0,btn_calculo_total)
                            }
                        } 
                        
                        contentItem: Item{
                            Text {
                                text: btn_calculo_total.text
                                font.pointSize: 11
                                font.bold: true
                                color: "#fff"
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.horizontalCenter: parent.horizontalCenter
                            }
                        }                        
                    }
                    Button{
                        id: btn_calculo_falla
                        property bool isrunning:false
                        Layout.alignment:Qt.AlignHCenter
                        Layout.preferredWidth: 200
                        text: qsTr("Comenzar")
                        opacity:5
                        Material.background: Material.color(Material.Green,Material.ShadeA700)
                        Material.elevation: 6
                        onClicked:{
                            if (isrunning){
                                backend.stop_falla_cc()
                                Material.background = Material.color(Material.Green,Material.ShadeA700)
                                btn_calculo_falla.text = "Comenzar"
                                btn_calculo_falla.isrunning=false

                            }else{
                                conections.verification(1,btn_calculo_falla)
                            }
                        } 
                        
                        contentItem: Item{
                            Text {
                                text: btn_calculo_falla.text
                                font.pointSize: 11
                                font.bold: true
                                color: "#fff"
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.horizontalCenter: parent.horizontalCenter
                            }
                        }                        
                    }
                    Button{
                        id: btn_calculo_garantia
                        property bool isrunning:false
                        Layout.alignment:Qt.AlignHCenter
                        Layout.preferredWidth: 200
                        text: qsTr("Comenzar")
                        opacity:5
                        Material.background: Material.color(Material.Green,Material.ShadeA700)
                        Material.elevation: 6
                        onClicked:{
                            if (isrunning){
                                backend.stop_garantia_cc()
                                Material.background = Material.color(Material.Green,Material.ShadeA700)
                                btn_calculo_garantia.text = "Comenzar"
                                btn_calculo_garantia.isrunning=false

                            }else{
                                conections.verification(2,btn_calculo_garantia)
                            }
                        } 
                        
                        contentItem: Item{
                            Text {
                                text: btn_calculo_garantia.text
                                font.pointSize: 11
                                font.bold: true
                                color: "#fff"
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.horizontalCenter: parent.horizontalCenter
                            }
                        }                        
                    }
                    Button{
                        id: btn_resultados_calculo_total
                        Layout.alignment:Qt.AlignHCenter
                        Layout.preferredWidth: 200
                        text: qsTr("Resultados")
                        opacity:5
                        
                        Material.background: Material.color(Material.Green,Material.ShadeA700)
                        Material.elevation: 6
                        enabled:false
                        flat:true
                        hoverEnabled:false
                        onClicked: conections.showResults_total()
                        contentItem: Item{
                            Text {
                                id:txt_resultados_calculo_total
                                text: btn_resultados_calculo_total.text
                                font.pointSize: 12
                                font.bold: true
                                color: "#fff"
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.horizontalCenter: parent.horizontalCenter
                            }
                        }                        
                    }
                    Button{
                        id: btn_resultados_calculo_falla
                        Layout.alignment:Qt.AlignHCenter
                        Layout.preferredWidth: 200
                        text: qsTr("Resultados")
                        Material.background:Material.color(Material.Yellow,Material.ShadeA700)
                        Material.elevation: 6

                        enabled:false
                        flat:true
                        hoverEnabled:false

                        opacity:5
                        onClicked: conections.showResults_falla()
                        contentItem: Item{
                            Text {
                                id:txt_resultados_calculo_falla
                                text: btn_resultados_calculo_falla.text
                                font.pointSize: 11
                                font.bold: true
                                color: "#fff"
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.horizontalCenter: parent.horizontalCenter
                            }
                        }                        
                    }
                    Button{
                        id: btn_resultados_calculo_garantia
                        Layout.alignment:Qt.AlignHCenter
                        Layout.preferredWidth: 200
                        text: qsTr("Resultados")
                        opacity:5
                        Material.background: Material.color(Material.Green,Material.ShadeA700)
                        Material.elevation: 6
                        enabled:false
                        flat:true
                        hoverEnabled:false
                        onClicked: conections.showResults_garantia()
                        contentItem: Item{
                            Text {
                                id:txt_resultados_calculo_garantia
                                text: btn_resultados_calculo_garantia.text
                                font.pointSize: 12
                                font.bold: true
                                color: "#fff"
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.horizontalCenter: parent.horizontalCenter
                            }
                        }                        
                    }
                    Button{
                        id: btn_exportar_calculo_total
                        Layout.alignment:Qt.AlignHCenter
                        Layout.preferredWidth: 200
                        text: qsTr("Exportar Excel")
                        opacity:5
                        
                        Material.background: Material.color(Material.Green,Material.ShadeA700)
                        Material.elevation: 6
                        enabled:false
                        flat:true
                        hoverEnabled:false
                        onClicked: backend.export_excel_total_cc()
                        
                        contentItem: Item{
                            Text {
                                id:txt_exportar_calculo_total
                                text: btn_exportar_calculo_total.text
                                font.pointSize: 12
                                font.bold: true
                                color: "#fff"
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.horizontalCenter: parent.horizontalCenter
                            }
                        }                        
                    }
                    Button{
                        id: btn_exportar_calculo_falla
                        Layout.alignment:Qt.AlignHCenter
                        Layout.preferredWidth: 200
                        text: qsTr("Exportar Excel")
                        Material.background:Material.color(Material.Yellow,Material.ShadeA700)
                        Material.elevation: 6

                        enabled:false
                        flat:true
                        hoverEnabled:false

                        opacity:5
                        onClicked: backend.export_excel_falla_cc()
                        contentItem: Item{
                            Text {
                                id:txt_exportar_calculo_falla
                                text: btn_exportar_calculo_falla.text
                                font.pointSize: 11
                                font.bold: true
                                color: "#fff"
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.horizontalCenter: parent.horizontalCenter
                            }
                        }                        
                    }
                    Button{
                        id: btn_exportar_calculo_garantia
                        Layout.alignment:Qt.AlignHCenter
                        Layout.preferredWidth: 200
                        text: qsTr("Exportar Excel")
                        opacity:5
                        Material.background: Material.color(Material.Green,Material.ShadeA700)
                        Material.elevation: 6
                        enabled:false
                        flat:true
                        hoverEnabled:false
                        onClicked: backend.export_excel_garantia_cc()
                        contentItem: Item{
                            Text {
                                id:txt_exportar_calculo_garantia
                                text: btn_exportar_calculo_garantia.text
                                font.pointSize: 12
                                font.bold: true
                                color: "#fff"
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.horizontalCenter: parent.horizontalCenter
                            }
                        }                        
                    }
                    Button{
                        id: btn_curva_calculo_total
                        Layout.alignment:Qt.AlignHCenter
                        Layout.preferredWidth: 200
                        text: qsTr("Curva Duración")
                        opacity:5
                        
                        Material.background: Material.color(Material.Green,Material.ShadeA700)
                        Material.elevation: 6
                        enabled:false
                        flat:true
                        hoverEnabled:false
                        onClicked: backend.curva_duracion_total_cc()
                        
                        contentItem: Item{
                            Text {
                                id:txt_curva_calculo_total
                                text: btn_curva_calculo_total.text
                                font.pointSize: 12
                                font.bold: true
                                color: "#fff"
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.horizontalCenter: parent.horizontalCenter
                            }
                        }                        
                    }
                    Button{
                        id: btn_curva_calculo_falla
                        Layout.alignment:Qt.AlignHCenter
                        Layout.preferredWidth: 200
                        text: qsTr("Curva Duración")
                        Material.background:Material.color(Material.Yellow,Material.ShadeA700)
                        Material.elevation: 6

                        enabled:false
                        flat:true
                        hoverEnabled:false

                        opacity:5
                        onClicked: backend.curva_duracion_falla_cc()
                        contentItem: Item{
                            Text {
                                id:txt_curva_calculo_falla
                                text: btn_curva_calculo_falla.text
                                font.pointSize: 11
                                font.bold: true
                                color: "#fff"
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.horizontalCenter: parent.horizontalCenter
                            }
                        }                        
                    }
                    Button{
                        id: btn_curva_calculo_garantia
                        Layout.alignment:Qt.AlignHCenter
                        Layout.preferredWidth: 200
                        text: qsTr("Curva Garantía")
                        opacity:5
                        Material.background: Material.color(Material.Green,Material.ShadeA700)
                        Material.elevation: 6
                        enabled:false
                        flat:true
                        hoverEnabled:false
                        onClicked: backend.curva_garantia_cc()
                        contentItem: Item{
                            Text {
                                id:txt_curva_calculo_garantia
                                text: btn_curva_calculo_garantia.text
                                font.pointSize: 12
                                font.bold: true
                                color: "#fff"
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.horizontalCenter: parent.horizontalCenter
                            }
                        }                        
                    }
                }

            }
        }
        
    }
    Connections {
        id:conections
        target: backend

        // CUSTOM PROPERTIES
        property var resultadosTotalCC
        property var resultadosFallaCC
        property var resultadosGarantiaCC

        function onSignalResultadosTotalCC(myResultadosTotalCC){resultadosTotalCC = myResultadosTotalCC}
        function onSignalResultadosFallaCC(myResultadosFallaCC){resultadosFallaCC = myResultadosFallaCC}
        function onSignalResultadosGarantiaCC(myResultadosGarantiaCC){resultadosGarantiaCC = myResultadosGarantiaCC}

        function onSignalFinishCC(myString){
            var btn
            var btn_resultados
            var btn_exportar
            var btn_curva
            var txt_resultados
            var txt_exportar
            var txt_curva

            if (myString == "total"){
                btn = btn_calculo_total
                btn_resultados = btn_resultados_calculo_total
                btn_exportar = btn_exportar_calculo_total
                btn_curva = btn_curva_calculo_total
                txt_resultados = txt_resultados_calculo_total
                txt_exportar = txt_exportar_calculo_total
                txt_curva = txt_curva_calculo_total
            }else if(myString == "falla"){
                btn = btn_calculo_falla
                btn_resultados = btn_resultados_calculo_falla
                btn_exportar = btn_exportar_calculo_falla
                btn_curva = btn_curva_calculo_falla
                txt_resultados = txt_resultados_calculo_falla
                txt_exportar = txt_exportar_calculo_falla
                txt_curva = txt_curva_calculo_falla
            }else if(myString == "garantia"){
                btn = btn_calculo_garantia
                btn_resultados = btn_resultados_calculo_garantia
                btn_exportar = btn_exportar_calculo_garantia
                btn_curva = btn_curva_calculo_garantia
                txt_resultados = txt_resultados_calculo_garantia
                txt_exportar = txt_exportar_calculo_garantia
                txt_curva = txt_curva_calculo_garantia
            }
            btn.Material.background = Material.color(Material.Green,Material.ShadeA700)
            btn.text = "Comenzar"
            btn.isrunning=false

            btn_resultados.Material.background=Material.color(Material.Yellow,Material.ShadeA700)
            btn_resultados.Material.elevation= 6
            btn_resultados.enabled=true
            btn_resultados.flat=false
            btn_resultados.hoverEnabled=true
            txt_resultados.color = "#000"

            btn_exportar.Material.background=Material.color(Material.Teal,Material.ShadeA700)
            btn_exportar.Material.elevation= 6
            btn_exportar.enabled=true
            btn_exportar.flat=false
            btn_exportar.hoverEnabled=true
            txt_exportar.color = "#000"

            btn_curva.Material.background=Material.color(Material.Cyan,Material.ShadeA700)
            btn_curva.Material.elevation= 6
            btn_curva.enabled=true
            btn_curva.flat=false
            btn_curva.hoverEnabled=true
            txt_curva.color = "#000"

        }

        // FUNCTION VERIFICATION
        function verification(indice,btn){

            var error = repeater_error.itemAt(indice)
            var range=lista_input[indice].length
            var info_completa = true
            var contador = 0
            var lim = parseInt(cant_variables[indice][contador])
            var data = []
            var info = []

            for(var i=0;i<range;i++){
                var input = repeater_input.itemAt(indice).children[0].children[0].children[0].children[i].children[1]
                if(input.text == ""){
                    error.text = "Todos los campos deben ser completados"
                    info_completa = false
                    break
                }
            }

            if(info_completa){
                error.text = ""
                btn.isrunning = true
                btn.Material.background = Material.color(Material.Pink,Material.ShadeA700)
                btn.text = "PARAR"
                for(var i=0;i<range;i++){
                    var input = repeater_input.itemAt(indice).children[0].children[0].children[0].children[i].children[1].text
                    input = parseFloat(input)
                    if(i < lim){
                        info.push(input)
                    }else{
                        data.push(info)
                        info = [input]
                        contador += 1
                        lim += parseInt(cant_variables[indice][contador])
                    }
                    if( i == range-1){
                        data.push(info)
                    }
                }

                if(indice == 0){backend.calculo_total_cc(data)}
                else if(indice == 1){backend.calculo_falla_cc(data)}
                else if(indice == 2){backend.calculo_garantia_cc(data)}
            }
            
        }

        // FUNCTION TO MANAGE ERRORS
        function onSignalErrorTotalCC(myError){
            var error = repeater_error.itemAt(0)
            error.text = myError
            btn_calculo_total.Material.background = Material.color(Material.Green,Material.ShadeA700)
            btn_calculo_total.text = "Comenzar"
            btn_calculo_total.isrunning=false
        }

        // FUNCTION TO OPEN NEW WINDOW (APP WINDOW)
        function showResults_total(){
            console.log(resultadosTotalCC)
            var component = Qt.createComponent("app.qml")
            var win = component.createObject()
            win.resultados = resultadosTotalCC
            win.show()
            visible = true
        }

        // FUNCTION TO MANAGE ERRORS
        function onSignalErrorFallaCC(myError){
            var error = repeater_error.itemAt(1)
            error.text = myError
            btn_calculo_falla.Material.background = Material.color(Material.Green,Material.ShadeA700)
            btn_calculo_falla.text = "Comenzar"
            btn_calculo_falla.isrunning=false
        }

        // FUNCTION TO OPEN NEW WINDOW (APP WINDOW)
        function showResults_falla(){
            var component = Qt.createComponent("app.qml")
            var win = component.createObject()
            win.resultados = resultadosFallaCC
            win.show()
            visible = true
        }
        // FUNCTION TO MANAGE ERRORS
        function onSignalErrorGarantiaCC(myError){
            var error = repeater_error.itemAt(2)
            error.text = myError
            btn_calculo_garantia.Material.background = Material.color(Material.Green,Material.ShadeA700)
            btn_calculo_garantia.text = "Comenzar"
            btn_calculo_garantia.isrunning=false
        }

        // FUNCTION TO OPEN NEW WINDOW (APP WINDOW)
        function showResults_garantia(){
            var component = Qt.createComponent("app.qml")
            var win = component.createObject()
            win.resultados = resultadosGarantiaCC
            win.show()
            visible = true
        }
    }
}