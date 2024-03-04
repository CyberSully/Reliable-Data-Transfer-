from segment import Segment

# Author -- Brett Sullivan
# Modified last -- 3-01-2024
# CS372 Networks

# Works Cited:

# https://pythonexamples.org/python-split-string-into-specific-length-chunks/
# https://www.baeldung.com/cs/networking-go-back-n-protocol
# https://www.youtube.com/watch?v=yNedVgNyE8Q&t=2s "Lec-25: Various Flow Control Protocols | Stop&Wait , GoBackN & Selective repeat in Data Link Layer"
# https://www.educative.io/courses/grokking-computer-networking/reliable-data-transfer-go-back-n
# https://www.geeksforgeeks.org/reliable-data-transfer-rdt-2-0/
# https://www.geeksforgeeks.org/sliding-window-protocol-set-3-selective-repeat/


# #################################################################################################################### #
# RDTLayer                                                                                                             #
#                                                                                                                      #
# Description:                                                                                                         #
# The reliable data transfer (RDT) layer is used as a communication layer to resolve issues over an unreliable         #
# channel.                                                                                                             #
#                                                                                                                      #
#                                                                                                                      #
# Notes:                                                                                                               #
# This file is meant to be changed.                                                                                    #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #


class RDTLayer(object):
    # ################################################################################################################ #
    # Class Scope Variables                                                                                            #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    # in characters                     # The length of the string data that will be sent per packet...
    DATA_LENGTH = 4
    # in characters          # Receive window size for flow-control
    FLOW_CONTROL_WIN_SIZE = 15
    sendChannel = None
    receiveChannel = None
    dataToSend = ''
    # Use this for segment 'timeouts'
    currentIteration = 0
    # Add items as needed
    # added variables below:
    currentWindow = [0, 4]
    currentSeqNum = 0
    expectedAck = 4
    iterationsWithoutAck = 0
    serverData = []

    # ################################################################################################################ #
    # __init__()                                                                                                       #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def __init__(self):
        self.sendChannel = None
        self.receiveChannel = None
        self.dataToSend = ''
        self.currentIteration = 0
        # Add items as needed
        # 6 lines added below
        self.countSegmentTimeouts = 0
        self.currAck = 0
        self.windowStart = 0
        self.windowEnd = 4
        self.role = "Server"
        self.waitTime = 0

    # ################################################################################################################ #
    # setSendChannel()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable sending lower-layer channel                                                 #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setSendChannel(self, channel):
        self.sendChannel = channel

    # ################################################################################################################ #
    # setReceiveChannel()                                                                                              #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable receiving lower-layer channel                                               #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setReceiveChannel(self, channel):
        self.receiveChannel = channel

    # ################################################################################################################ #
    # setDataToSend()                                                                                                  #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the string data to send                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setDataToSend(self, data):
        self.dataToSend = data

    # ################################################################################################################ #
    # getDataReceived()                                                                                                #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to get the currently received and buffered string data, in order                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def getDataReceived(self):
        # Identify the data that has been received...

        print('getDataReceived():')
        # Sort the received data by sequence number
        dataSorted = sorted(self.serverData)

        # Concatenate the payloads of sorted data into a single string
        stringSorted = ""
        for i in range(len(dataSorted)):
            stringSorted += dataSorted[i][1]

        return stringSorted

    # ################################################################################################################ #
    # processData()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # "timeslice". Called by main once per iteration                                                                   #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #

    def processData(self):
        self.currentIteration += 1
        self.processSend()
        self.processReceiveAndSendRespond()

    # ################################################################################################################ #
    # processSend()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment sending tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #

    # ~~~~~~~~~~~~~~~~~~~~~~~~ Heavily Edited Function ~~~~~~~~~~~~~~~~~~~~~~

    def processSend(self):
        print('processSend(): Implement this...')
        # Set role to client if there is data to send
        if self.dataToSend:
            self.role = "Client"

        # Split data into segments of specified length
        split_data = [self.dataToSend[i:i + self.DATA_LENGTH]
                      for i in range(0, len(self.dataToSend), self.DATA_LENGTH)]

        # Handle retransmission timeout
        if self.currentIteration > 1 and not self.receiveChannel.receiveQueue:
            if self.waitTime == 3:
                # Resend current window if timeout limit reached
                self.currentSeqNum = self.currentWindow[0]
                self.countSegmentTimeouts += 1
            else:
                # Increment timeout counter
                self.waitTime += 1
                return

        # Check for received acknowledgments
        if self.receiveChannel.receiveQueue and self.role == "Client":
            acklist = self.receiveChannel.receive()
            self.checkReceivedAck(acklist)

        # Set window start and end sequence numbers
        seqnum = self.currentSeqNum
        self.winStart = seqnum
        self.winEnd = seqnum + 4

        # Send data segments if not in server role
        if self.role != "server":
            self.sendData(self.winStart, self.winEnd, seqnum,
                          split_data, len(split_data))

    # ~~~~~~~~~~~ Added Function for checking recieved Acks ~~~~~~~~~~~~~~~~~~~~~~~

    def checkReceivedAck(self, toCheck):
        # Iterate over the list of segments to check acknowledgment numbers
        for segment in toCheck:
            # Check if the acknowledgment number matches the expected acknowledgment
            if segment.acknum == self.expectedAck:
                # Increment sequence numbers, acknowledgment numbers, and window boundaries
                self.currentSeqNum += 4
                self.expectedAck += 4
                self.currentWindow[0] += 4
                self.currentWindow[1] += 4

    # ~~~~~~~ Added Function for sending packets of items from window start to window end, sends on channel ~~~~~~~~~~~~~~~~~

    def sendData(self, wStart, wEnd, seqnum, dataArr, dataSize):
        # Iterate over the window range
        for i in range(wStart, wEnd):
            # Check if there is data to send and the sequence number is within the range of data array
            if self.dataToSend and seqnum < len(dataArr):
                # Create a new segment
                segmentSend = Segment()

                # Retrieve data from the data array
                data = dataArr[seqnum]

                # Set data and sequence number in the segment
                segmentSend.setData(seqnum, data)
                seqnum += 1

                # Set start iteration and delay iteration in the segment
                segmentSend.setStartIteration(self.currentIteration)
                segmentSend.setStartDelayIteration(4)

                # Send the segment through the send channel
                self.sendChannel.send(segmentSend)

    # ################################################################################################################ #
    # processReceive()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment receive tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #

     # ~~~~~~~~~~~~~~~~~~~~~~~~Heavily Edited Function ~~~~~~~~~~~~~~~~~~~~~~

    def processReceiveAndSendRespond(self):

        # Receive incoming segments from the receive channel
        listIncomingSegments = self.receiveChannel.receive()

        print('processReceive(): Complete this...')

        # Check if there are any incoming segments
        if (len(listIncomingSegments) > 0):
            # Create a new segment to send acknowledgment
            segmentAck = Segment()

            # Initialize current acknowledgment number
            currentAck = self.currentWindow[0]

            # Update the expected acknowledgment number
            self.expectedAck = self.currentWindow[1]

            # Process the received segments to remove duplicates and calculate acknowledgment
            newList, recAck = self.processReceivedList(
                listIncomingSegments)

            # Increment the current acknowledgment by the received acknowledgment
            currentAck += recAck

            # Check if the current acknowledgment matches the expected acknowledgment
            if (currentAck == self.expectedAck):
                # Move the window start by 4 and update the current acknowledgment
                self.winStart += 4
                self.currAck = self.currAck + 4

                # Set acknowledgment in the segment and send it
                segmentAck.setAck(currentAck)
                # should send cumulative acknum
                self.sendChannel.send(segmentAck)

            # Add the new segments to the server data if not already present to avoid duplicates
            self.addNewListToServerData(newList)
        else:
            return

  # ~~~~~~~ Added Function for removing duplicate items and ones that dont pass checksum ~~~~~~~~

    def processReceivedList(self, toProcess):
        # Initialize empty lists to store sequence numbers and payloads
        seqAndPayloadList = []
        uniqueToProcess = []

        # Iterate over each segment in the received list
        for i in range(len(toProcess)):
            # Check if the payload is not empty and if the checksum passes
            if (toProcess[i].payload != "" and toProcess[i].checkChecksum() == True):
                # If conditions are met, append the sequence number and payload to the list
                seqAndPayloadList.append(
                    [toProcess[i].seqnum, toProcess[i].payload])

        # Iterate over each item in the sequence and payload list
        for j in range(len(seqAndPayloadList)):
            # Check if the item is not already in the unique list and if it falls within the current window
            if (seqAndPayloadList[j] not in uniqueToProcess and (self.currentWindow[0] <= seqAndPayloadList[j][0] <= self.currentWindow[1])):
                # If conditions are met, append the item to the unique list
                uniqueToProcess.append(seqAndPayloadList[j])

        # Calculate the number of unique packets remaining and return the unique list along with its length
        return uniqueToProcess, len(uniqueToProcess)

    # ~~~~~~~~~~~~~~~~~~~ Added Function for going through list adding server data vairable w ssequence and payload for sorting

    def addNewListToServerData(self, toAdd):
        # Iterate over each item in the list to add
        for i in range(len(toAdd)):
            # Check if the item is not already in the server data
            if toAdd[i] not in self.serverData:
                # If condition is met, append the item to the server data
                self.serverData.append(toAdd[i])
