"
Observer interface for ContextRecorderDecorator
"
Class {
	#name : 'ContextRecordedObserver',
	#superclass : 'Object',
	#category : 'Tracing',
	#package : 'Tracing'
}

{ #category : 'notifications' }
ContextRecordedObserver >> notifyInstanceVariableOfCurrentObject: anInstVarName isAssigned: aVarNamed [
	
	^self subclassResponsibility 
]

{ #category : 'notifications' }
ContextRecordedObserver >> notifyLiteralVariableAssigmentTo: aVariableName of: aLiteralValueName [

	^self subclassResponsibility 
]

{ #category : 'notifications' }
ContextRecordedObserver >> notifyMessageSentTo: recieverName withSelector: selector andArguments: argumentsNames [

	^self subclassResponsibility 
]

{ #category : 'notifications' }
ContextRecordedObserver >> notifyOfVolatileAssigmentOf: aVolatileVariableName with: aVariableName [

	^self subclassResponsibility 
]

{ #category : 'notifications' }
ContextRecordedObserver >> notifyTemporaryVariableAssignmentOf: aTempVar with: aVolatileVar [

	^self subclassResponsibility 
]

{ #category : 'notifications' }
ContextRecordedObserver >> notifyVolatileVariable: aVolatileVariableName isAssignedInstanceVariable: anInstanceVariableName [

	^self subclassResponsibility 
]
