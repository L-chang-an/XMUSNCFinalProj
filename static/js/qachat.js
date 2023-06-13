    $(document).ready(function() {
        var chatBtn = $('#chatBtn');
        var chatInput = $('#chatInput');
        var chatWindow = $('#chatWindow');
        var userIcon = '/static/images/avator/myicon.jpg'
        var botIcon = '/static/images/avator/gpticon.jpg';


        // 添加用户消息到窗口
        function addUserMessage(message) {
          var messageElement = $('<div class="row message-bubble"><img class="chat-icon" src="' + userIcon + '"><p class="message-text">' + message + '</p></div>');
          chatWindow.append(messageElement);
          chatInput.val('');
          chatWindow.animate({ scrollTop: chatWindow.prop('scrollHeight') }, 500);
        }

        // 添加回复消息到窗口
        function addBotMessage(message) {
          var messageElement = $('<div class="row message-bubble"><img class="chat-icon" src="' + botIcon + '"><p class="message-text">' + message + '</p></div>');
          chatWindow.append(messageElement);
          chatInput.val('');
          chatWindow.animate({ scrollTop: chatWindow.prop('scrollHeight') }, 500);
        }

        // 处理用户输入
        chatBtn.click(function() {
          var message = chatInput.val();
          if (message.length === 0){
            common_ops.alert("请输入内容！")
            return
          }
          addUserMessage(message);

          // messages.push({"role": "user", "content": message})

          chatBtn.attr('disabled',true) // 消息发送后让提交按钮不可点击
          // 发送信息到后台
          $.ajax({
            url: '/getAnswering',
            method: 'POST',
            data: {
              "prompt": JSON.stringify(message),
            },
            dataType: "json",
            success: function(res) {
              addBotMessage(res.content);
              chatBtn.attr('disabled',false)  // 成功接受消息后让提交按钮再次可以点击
            },
            error: function(jqXHR, textStatus, errorThrown) {
              addBotMessage('<span style="color:red;">' + '出错啦！请稍后再试!' + '</span>');
              chatBtn.attr('disabled',false)
            }
          });
        });

        // 处理 Enter 键按下
        chatInput.keypress(function(e) {
          if (e.which === 13) {
            chatBtn.click();
          }
        });
  });