"
Class that connects Tracer with the outside
"
Class {
	#name : 'Connector',
	#superclass : 'ContextRecordedObserver',
	#instVars : [
		'socket',
		'client',
		'executionRecord',
		'context',
		'contextRecorder',
		'debug',
		'stream'
	],
	#classInstVars : [
		'socket',
		'client',
		'context'
	],
	#category : 'Tracing',
	#package : 'Tracing'
}

{ #category : 'testing' }
Connector >> context [
	^context 
]

{ #category : 'testing' }
Connector >> debug [
	^debug 
]

{ #category : 'testing' }
Connector >> executionRecord [

	^executionRecord copy
]

{ #category : 'event handling' }
Connector >> getObjectOfName: anObjectName [

	| object |
	(anObjectName isNumber ) ifTrue: [ ^anObjectName ].
	(context includesKey: anObjectName ) ifTrue: [ 
			object := context at: anObjectName .
		 ] ifFalse: [ 
				Smalltalk globals allClassesDo: 
					[ :class |	
					(class name = anObjectName asSymbol) ifTrue: [ object := class. ].
		 ].
	].
^object
]

{ #category : 'initialization' }
Connector >> initialize [ 

	socket := Socket newTCP .
	
	context := Dictionary new.
	executionRecord := OrderedCollection new.
	
	
	
	
	
]

{ #category : 'notifications' }
Connector >> notifyInstanceVariableOfCurrentObject: anInstVarName isAssigned: aVarNamed [
	
	^self recordThat: anInstVarName isBeignAssigned: aVarNamed 
]

{ #category : 'notifications' }
Connector >> notifyLiteralVariableAssigmentTo: aVariableName of: aLiteralValueName [

	^self recordThat: aVariableName isBeignAssigned: aLiteralValueName 
]

{ #category : 'notifications' }
Connector >> notifyMessageSentTo: recieverName withSelector: selector andArguments: argumentsNames [

	
	executionRecord add: (Dictionary newFrom: { 
													'type' -> 'send'.
													'reciever' -> recieverName.
													'selector' -> selector .
													'arguments' -> argumentsNames 
												 })
	
	
	
]

{ #category : 'notifications' }
Connector >> notifyOfVolatileAssigmentOf: aVolatileVariableName with: aVariableName [

	^self recordThat: aVolatileVariableName isBeignAssigned: aVariableName 
]

{ #category : 'notifications' }
Connector >> notifyTemporaryVariableAssignmentOf: aTempVar with: aVolatileVar [

	^self recordThat: aTempVar isBeignAssigned: aVolatileVar 
]

{ #category : 'notifications' }
Connector >> notifyVolatileVariable: aVolatileVariableName isAssignedInstanceVariable: anInstanceVariableName [

	^self recordThat: aVolatileVariableName isBeignAssigned: anInstanceVariableName 
]

{ #category : 'notifications' }
Connector >> recordThat: aName isBeignAssigned: anotherName [
	executionRecord 
		add: (Dictionary newFrom: {
											'type' -> 'assignment'.
											'to' -> aName .
											'from' -> anotherName 									
										}).
]

{ #category : 'event handling' }
Connector >> startConnection [

	socket listenOn: 9290 backlogSize: 10.
	Transcript showCr: 'Trying to start connection'.
	[
		client := socket
			          waitForAcceptFor: 16
			          ifClosed: [ 'CLOSED' ]
			          ifTimedOut: [ 'TIMEOUT' ].
		stream := SocketStream on: client.
		
		[ client isString not and: [ client isConnected ] ] whileTrue: [
				self waitForMessage.
				stream sendCommand: (NeoJSONWriter toString: executionRecord).
				executionRecord removeAll ] 
			] ensure: [
			
			Transcript showCr: 'Closing connection'.
			socket closeAndDestroy.
			stream ifNotNil:[ stream close ]]
]

{ #category : 'event handling' }
Connector >> waitForMessage [

	| request parsedResponse temporaryVariable senderName selectorName argumentsNames sender selector arguments answer |
	request := stream nextLineLf .
	Transcript
		showCr: 'Received request: ', request asString.
		
	parsedResponse := NeoJSONReader fromString: request.

	temporaryVariable := parsedResponse at: 'variable'.
	senderName := parsedResponse at: 'receiver'.
	selectorName := parsedResponse at: 'selector'.
	argumentsNames := parsedResponse at: 'arguments'.
	
	
	sender := self getObjectOfName: senderName.
	
	selector := selectorName asSymbol .
		
	arguments := argumentsNames collect: [ :argumentsName | self getObjectOfName: argumentsName ].
	
	Transcript 
		show: sender asString;
		show:' ';
		show: selector asString;
		show:' ';
		show: arguments asString;
		cr.
	
	contextRecorder := ContextRecordedDecorator with: thisContext.
	
	
	contextRecorder addObserver: self .
	contextRecorder runSimulated: [ answer := sender perform: selector withArguments:arguments ].
	
	Transcript showCr: 'Successfully simulated request'.
	
	context at: temporaryVariable put: answer 
	
	

	
]
