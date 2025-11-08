Class {
	#name : 'ObserverStream',
	#superclass : 'ContextRecordedObserver',
	#instVars : [
		'registry'
	],
	#category : 'Tracing',
	#package : 'Tracing'
}

{ #category : 'initialization' }
ObserverStream >> initialize [ 

	registry := OrderedCollection new.
]

{ #category : 'notifications' }
ObserverStream >> notifyInstanceVariableOfCurrentObject: anInstVarName isAssigned: aVarNamed [
	
	self recordThat: anInstVarName isBeignAssigned: aVarNamed 
]

{ #category : 'notifications' }
ObserverStream >> notifyLiteralVariableAssigmentTo: aVariableName of: aLiteralValueName [

	self recordThat: aVariableName isBeignAssigned: aLiteralValueName 
]

{ #category : 'notifications' }
ObserverStream >> notifyMessageSentTo: recieverName withSelector: selector andArguments: argumentsNames [
	|sendMessage|
	
	sendMessage := recieverName , ' ' , selector, ' '.
	argumentsNames do: [ :argumentName | sendMessage := sendMessage, argumentName, ', ' ].
	
	registry
		add: sendMessage.
]

{ #category : 'notifications' }
ObserverStream >> notifyOfVolatileAssigmentOf: aVolatileVariableName with: aVariableName [

	self recordThat: aVolatileVariableName isBeignAssigned: aVariableName 
]

{ #category : 'notifications' }
ObserverStream >> notifyTemporaryVariableAssignmentOf: aTempVar with: aVolatileVar [

	self recordThat: aTempVar isBeignAssigned: aVolatileVar 
]

{ #category : 'notifications' }
ObserverStream >> notifyVolatileVariable: aVolatileVariableName isAssignedInstanceVariable: anInstanceVariableName [

	self recordThat: aVolatileVariableName isBeignAssigned: anInstanceVariableName .
]

{ #category : 'accessing' }
ObserverStream >> record [

	^registry 
]

{ #category : 'private' }
ObserverStream >> recordThat: aName isBeignAssigned: anotherName [
	registry
		add: (aName , ' := ' , anotherName).
]
