class Script {
	prepare_outgoing_request({ request }) {
      	var content = request.data.text;
	    var split_content = content.split("\n");
        var form_content = split_content[0];
        var form_link = form_content.substring(7);
        var jobNum = split_content[2];
        var jobLink = split_content[3];
        var type = split_content[4];
        var customer = split_content[1];
	    let x = Math.floor(Math.random() * 10000) + 1;
      	let msg = {
          text: type + ' Please click the link to view the parts order form for customer: ' + customer + " -- REF#" + x + "",
          attachments: [
            {
              color: '#0000DD',
              title: "Job requires parts",
              text: "[GOTO PARTS ORDER FORM](" + form_link + ") \n" + "[GOTO JOB #" + jobNum + "](" + jobLink + ")",
              button_alignment: "horizontal",
              image_url: "YourActionCardURL",
              actions: [
                {
                  type: "button",
                  text: "I GOT THIS",
                  msg_in_chat_window: true,
                  msg: "@PartsBot GOT IT (Customer: " + customer + ") REF#" + x,
                  mentions: [ "Rocket.Cat" ]
                }
              ]
            }
          ]
        };
		return { message: msg };
	}
	process_outgoing_response({ request, response }) {
	}
}
