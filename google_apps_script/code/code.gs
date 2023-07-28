function doGet() {
  //return HtmlService.createHtmlOutput("<b>hello</b>");
  return countEmailsBySender();
}

function countEmailsBySender() {
  var threads = GmailApp.search('after:' + getThreeMonthsAgoDate());
  var senderCount = {};

  for (var i = 0; i < threads.length; i++) {
    var messages = threads[i].getMessages();
    for (var j = 0; j < messages.length; j++) {
      var sender = messages[j].getFrom();
      if (senderCount[sender]) {
        senderCount[sender]++;
      } else {
        senderCount[sender] = 1;
      }
    }
  }

  var sortedSenders = Object.keys(senderCount).sort(function(a, b) {
    return senderCount[b] - senderCount[a];
  });

  var htmlOutput = HtmlService.createTemplateFromFile('emailCountTemplate');
  htmlOutput.senders = sortedSenders;
  htmlOutput.counts = sortedSenders.map(function(sender) {
    return senderCount[sender];
  });

  var html = htmlOutput.evaluate().setTitle('Email Count by Sender');
  //SpreadsheetApp.getUi().showModalDialog(html, 'Email Count by Sender');
  return html;
}

function getThreeMonthsAgoDate() {
  var today = new Date();
  var threeMonthsAgo = new Date(today.getFullYear(), today.getMonth() - 3, today.getDate());
  var dateString = Utilities.formatDate(threeMonthsAgo, Session.getScriptTimeZone(), 'yyyy/MM/dd');
  return dateString;
}
