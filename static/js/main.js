
function call_broker_project(){

       description = $('#validacao').val()
       payload = {
            "microservice": "project",
            "payload": { "description": description }
       }

       $.ajax({
          url: "/broker",
          type: "PUT",
          contentType: 'application/json',
          dataType: 'json',
          data: JSON.stringify(payload),
          success: function(response) {
            if(response.code != '200')
                window.alert('Erro ao atualizar:\n' + response.message);
            else {
                window.alert('Registro atualizado com sucesso!');
                location.reload();
            }
            console.log('sucess')
          },
          error: function(response) {
            window.alert('Erro ao atualizar:\n' + response);
            console.log('error')
          }
       });

}

function call_broker_system_general_features(){

       values = $('input[type=number]');

       var x, size = values.length;

       var payload = {}

       for (x=0; x<=size; x++){
          payload[$(values[x]).attr('name')] = $(values[x]).val()
       }
       payload['project_id'] = $('#projects').children('option:selected').val();

       payload = {
            "microservice": "system_general_features",
            "payload": { payload }
       }

       $.ajax({
          url: "/broker",
          type: "PUT",
          contentType: 'application/json',
          dataType: 'json',
          data: JSON.stringify(payload),
          success: function(response) {
            if(response.code != '200')
                window.alert('Erro ao atualizar:\n' + response.message);
            else {
                window.alert('Registro atualizado com sucesso!');
                location.reload();
            }
            console.log('sucess')
          },
          error: function(response) {
            window.alert('Erro ao atualizar:\n' + response);
            console.log('error')
          }
       });

}

function call_broker_tdd(){

       expected = $('#expected').val();

       if (expected == 0.7) window.alert("Teste passou!")
       else window.alert("Teste falhou! Esperado era: 0.7")



}
