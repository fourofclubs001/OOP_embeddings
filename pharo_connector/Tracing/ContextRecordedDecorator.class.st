"
Context wrapper
"
Class {
	#name : 'ContextRecordedDecorator',
	#superclass : 'Object',
	#instVars : [
		'context',
		'observers',
		'stack'
	],
	#category : 'Tracing',
	#package : 'Tracing'
}

{ #category : 'initialization' }
ContextRecordedDecorator class >> with: aContext [

	^self new initializeWith: aContext 
]

{ #category : 'private' }
ContextRecordedDecorator >> addCurrentContextHashTo: aString [

	^self currentContextAsHash , '_', aString 
]

{ #category : 'observer' }
ContextRecordedDecorator >> addObserver: anObserver [

	observers add: anObserver .
]

{ #category : 'accessing' }
ContextRecordedDecorator >> context [
	^context 
]

{ #category : 'private' }
ContextRecordedDecorator >> currentContextAsHash [

	^(context stack collect: [ :contextStacked | contextStacked asString ]) hash asString 
]

{ #category : 'wrapping bytecode' }
ContextRecordedDecorator >> doPop [
	
	^context doPop
]

{ #category : 'other calls' }
ContextRecordedDecorator >> doesNotUnderstand: aMessage [
	
	^aMessage sendTo: context 
]

{ #category : 'private' }
ContextRecordedDecorator >> getNameOfVariable: stackIndex [
	
	|numberOfArguments numberOfTemps baseName name|
	
	numberOfArguments := context arguments size .
	numberOfTemps  := context temporaryVariables size.
	
	(stackIndex <= numberOfArguments) ifTrue: [ 
				baseName := context method argumentNames at: stackIndex 
			
		 ].
	(stackIndex > numberOfArguments and: stackIndex <= (numberOfTemps + numberOfArguments )) ifTrue: [ 
			baseName := (context temporaryVariables at: stackIndex - numberOfArguments ) asString
		 ].
	
	(stackIndex > (numberOfTemps + numberOfArguments)) ifTrue: [ 
			baseName := 'volatile_', (stackIndex - numberOfArguments - numberOfTemps ) asString.
		 ].
	
	name := self currentContextAsHash , '_', baseName .
	
	^name.
]

{ #category : 'initialization' }
ContextRecordedDecorator >> initializeWith: aContext [
	
	context := aContext .
	observers := OrderedCollection new.
	
	^self
]

{ #category : 'private' }
ContextRecordedDecorator >> nameOfLastVolatileVariable [

	^self getNameOfVariable: context stackPtr
]

{ #category : 'private' }
ContextRecordedDecorator >> nameOfReceiverInstanceVariableByOffset: offset [

	^ 'instanceVariable_', (context receiver class allInstVarNames at:offset +1 ) asString.
]

{ #category : 'wrapping bytecode' }
ContextRecordedDecorator >> popIntoReceiverVariable: offset [
	
	|nameOfInstVar|
	
	
	nameOfInstVar := self nameOfReceiverInstanceVariableByOffset: offset.
	
	observers do: [ :observer | observer notifyInstanceVariableOfCurrentObject: (self addCurrentContextHashTo: nameOfInstVar) isAssigned: self nameOfLastVolatileVariable ].

	^context popIntoReceiverVariable: offset
]

{ #category : 'wrapping bytecode' }
ContextRecordedDecorator >> popIntoTemporaryVariable: offset [
	observers do: [ :obs | obs notifyTemporaryVariableAssignmentOf: (self getNameOfVariable: offset + 1) with: self nameOfLastVolatileVariable  ].
	^context popIntoTemporaryVariable: offset
]

{ #category : 'wrapping bytecode' }
ContextRecordedDecorator >> pushLiteralVariable: value [
	
	observers do: [ :observer | observer notifyLiteralVariableAssigmentTo: (self getNameOfVariable: context stackPtr +1) of: value name asString ].
	
	^context pushLiteralVariable: value.
]

{ #category : 'wrapping bytecode' }
ContextRecordedDecorator >> pushReceiverVariable: offset [
	
	|nameOfInstVar|
	
	
	nameOfInstVar := self nameOfReceiverInstanceVariableByOffset: offset.
	
	observers do: [ :observer | observer notifyVolatileVariable: (self getNameOfVariable: context stackPtr + 1) isAssignedInstanceVariable: nameOfInstVar ].

	^context pushReceiverVariable: offset .
]

{ #category : 'wrapping bytecode' }
ContextRecordedDecorator >> pushTemporaryVariable: offset [
	
	observers do: [ :observer | observer notifyOfVolatileAssigmentOf: (self getNameOfVariable: context stackPtr + 1) with: (self getNameOfVariable: offset + 1) ].
	
	^context pushTemporaryVariable: offset 
]

{ #category : 'simulation' }
ContextRecordedDecorator >> runSimulated: aBlock [ 
	
	^self runSimulated: aBlock contextAtEachStep: [ :ignore| ] 
]

{ #category : 'simulation' }
ContextRecordedDecorator >> runSimulated: aBlock contextAtEachStep: block2 [
	"Simulate the execution of the argument, aBlock, until it ends. aBlock 
	MUST NOT contain an '^'. Evaluate block2 with the current context 
	prior to each instruction executed. Answer the simulated value of aBlock."
	| current returnContext exception decoratedContext |
	
	
	aBlock hasNonLocalReturn
		ifTrue: [ self error: 'simulation of blocks with ^ can run loose' ].
		
	current := [ aBlock
					on: Exception
					do: [ :ex | SimulationExceptionWrapper signalForException: ex  ] ] asContext.
	
	returnContext := Context
			sender: nil
			receiver: context home receiver
			method: context home compiledCode
			arguments: context home arguments.
	
	current pushArgs: Array new from: returnContext.
	
	decoratedContext := self class with: current.
	
	observers do: [ :observer | decoratedContext addObserver: observer ].
	
	[decoratedContext context == returnContext]
		whileFalse: [ 
			block2 value: decoratedContext context.
			decoratedContext := decoratedContext step ].
	
	exception := returnContext pop.
	exception class == SimulationExceptionWrapper
		ifTrue: [ ^ exception exception signal ].
	^ exception
]

{ #category : 'wrapping bytecode' }
ContextRecordedDecorator >> send: selector super: superFlag numArgs: numArgs [

	| argumentsNames recieverName |
	
	
	argumentsNames := OrderedCollection new.
	numArgs to: 1 by: -1 do: [ :index |
			argumentsNames add:
				(self getNameOfVariable: context stackPtr - index +1 ) ].
	recieverName := superFlag
		                ifTrue: [ 'super' ]
		                ifFalse: [
		                self getNameOfVariable: context stackPtr - numArgs  ].


	observers do: [ :observer |
			observer
				notifyMessageSentTo: recieverName
				withSelector: selector
				andArguments: argumentsNames ].

	^ context send: selector super: superFlag numArgs: numArgs
]

{ #category : 'wrapping bytecode' }
ContextRecordedDecorator >> step [
	"Simulate the execution of the receiver's next bytecode. Answer the
	context that would be the active context after this bytecode."
	<reflection: 'Stack Manipulation - Controlling the stack'>
	| stream result updatedContextRecorder |
	stream := InstructionStream on: context method pc: context pc.
	result := stream interpretNextInstructionFor: self.
	
	updatedContextRecorder := self class with: result.
	
	observers do: [ :observer | updatedContextRecorder addObserver: observer ].
	^updatedContextRecorder 
]
