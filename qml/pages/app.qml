import QtQuick 6
import QtQuick.Window 2.15
import QtQuick.Controls 6
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts

ApplicationWindow{
    id:window
    width: 600
    height: 500
    visible: true
    title: qsTr("Resultados")

    // SET MATERIAL STYLE
    Material.theme: Material.Dark
    Material.accent: Material.LightBlue

    // CUSTOM PROPERTIES
    property var resultados: []

    Rectangle {
        id: rectangleTop
        //height: 69
        //color: "#495163"
        color: "#2c313c"
        radius: 10
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.rightMargin: 50
        anchors.leftMargin: 100
        anchors.topMargin: 50
        ScrollView{
            anchors.fill: parent
            width: parent.width
            height: parent.height
            clip : true
            GridLayout{
                flow:GridLayout.TopToBottom
                rows:2
                rowSpacing:50
                columnSpacing:50
                Repeater{
                    model:resultados
                    Column{
                        spacing:10
                        Repeater{
                            model:modelData
                            Text{
                                text: modelData
                                //anchors.verticalCenter: parent.verticalCenter
                                //horizontalAlignment: Text.AlignHCenter
                                //verticalAlignment: Text.AlignVCenter
                                color:"#ffffff"
                                //anchors.horizontalCenter: parent.horizontalCenter
                                font.pointSize: 11
                            }
                        }
                    }
                }
            }
        }
        
        
    }
}


/* GridLayout{
    spacing:10
    columns:3
    Repeater{
        model:resultados
        Repeater{
            model:modelData
            Text{
                text: modelData
                //anchors.verticalCenter: parent.verticalCenter
                //horizontalAlignment: Text.AlignHCenter
                //verticalAlignment: Text.AlignVCenter
                color:"#ffffff"
                //anchors.horizontalCenter: parent.horizontalCenter
                font.pointSize: 11
            }
        }
    }
} */