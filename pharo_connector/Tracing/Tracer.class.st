"
Clase para obtener primer nivel de trace de un método
"
Class {
	#name : 'Tracer',
	#superclass : 'Object',
	#classInstVars : [
		'hola'
	],
	#category : 'Tracing',
	#package : 'Tracing'
}

{ #category : 'generic traces' }
Tracer class >> forEveryContextIn: aBlockToExecute atDepth: depth do: anActionBlock [

	self forEveryContextIn: aBlockToExecute do: [ :context | 
				(context depthBelow: aBlockToExecute ) = depth ifTrue: [ 
							anActionBlock value: context
					 ]
		 ]

]

{ #category : 'generic traces' }
Tracer class >> forEveryContextIn: aBlockToExecute do: anActionBlock [

	| previousContext  |
	
	
	previousContext := aBlockToExecute.
	thisContext sender
		runSimulated: aBlockToExecute
		contextAtEachStep: [ :current |
				current == previousContext ifFalse: [ 
							self halt.
							previousContext sender ifNotNil: [
								anActionBlock value: current.
								  ].
							previousContext := current] ].

]

{ #category : 'generic traces' }
Tracer class >> forEveryContextIn: aBlockToExecute fromDepth: depth do: anActionBlock [

	self forEveryContextIn: aBlockToExecute do: [ :context | 
				(context depthBelow: aBlockToExecute ) >=depth ifTrue: [ 
							anActionBlock value: context
					 ]
		 ]

]

{ #category : 'text output traces' }
Tracer class >> forSender: anObject selector: aSelector withArguments: aCollectionOfArguments [

	self forEveryContextIn: [ anObject perform: aSelector withArguments: aCollectionOfArguments ] fromDepth: 8 do: [ :currentContext|
				|responseDictionary|
				responseDictionary := Dictionary new 
				at: 'sender' put: currentContext receiver class name;
				at: 'messageSelector' put: currentContext selector;
				at: 'messageArguments' put: currentContext arguments.
		 ]
]

{ #category : 'private' }
Tracer class >> fromContext: aContext printOn: aStream [

aStream nextPutAll: (aContext receiver class name).
aStream space.
aStream nextPutAll:  aContext selector 

]

{ #category : 'text output traces' }
Tracer class >> getASTTraceFor: aBlock [

	|resultStream previousContext|
	resultStream := WriteStream on: ''.
	hola.
	
	
	previousContext := aBlock.
	thisContext sender
		runSimulated: aBlock
		contextAtEachStep: [:context |
			context == previousContext ifFalse: [ 
			((context depthBelow: aBlock) =5 or: (context depthBelow: aBlock ) =6) ifTrue:[
				
				((context method sourceNodeForPC: context pc) class = OCAssignmentNode ) ifTrue: [ 
					
										resultStream nextPut: Character cr.
							resultStream nextPutAll: 'Hay asignacion'
					 ].
				(previousContext sender) ifNotNil: [ 
			"resultStream nextPut: Character cr.
			(context depthBelow: aBlock) timesRepeat: [resultStream space]."
			resultStream nextPut: Character cr.
			self fromContext: context printOn: resultStream.
			"resultStream nextPutAll: (context method sourceNodeForPC: context pc) asString."
			]]. previousContext := context].
		 ] .
	^resultStream 
]

{ #category : 'text output traces' }
Tracer class >> getFirstLevelTraceOf: aBlock [

	| resultStream |
	
	resultStream := WriteStream on: String new.
	
	self forEveryContextIn: aBlock fromDepth: 6 do: [ :currentContext |
					
					resultStream nextPut: Character cr.
					self fromContext: currentContext printOn: resultStream.
		 ].
	^ resultStream
]

{ #category : 'text output traces' }
Tracer class >> getRawTraceOf: aBlock [
		| prev aStream|
		aStream := WriteStream on: String new.
	prev := aBlock.
	thisContext sender
		runSimulated: aBlock
		contextAtEachStep: [ :current |
			
			current == prev
				ifFalse: [
					prev sender ifNil: [
						aStream space; nextPut: $^.
						Context carefullyPrint: current top on: aStream].
					aStream nextPut: Character cr.
					(current depthBelow: aBlock) timesRepeat: [aStream space].
					Context carefullyPrint: current receiver on: aStream.
					aStream space; nextPutAll: current selector.
					prev := current]].
			^aStream 
			
]

{ #category : 'custom trace' }
Tracer class >> getRawTraceUsingDecoratorOf: aBlock [
		| prev aStream|
		aStream := WriteStream on: String new.
	prev := aBlock.
	(ContextRecordedDecorator with:( thisContext sender))
		runSimulated: aBlock
		contextAtEachStep: [ :current |
			
			current == prev
				ifFalse: [
					prev sender ifNil: [
						aStream space; nextPut: $^.
						Context carefullyPrint: current top on: aStream].
					aStream nextPut: Character cr.
					(current depthBelow: aBlock) timesRepeat: [aStream space].
					Context carefullyPrint: current receiver on: aStream.
					aStream space; nextPutAll: current selector.
					prev := current]].
			^aStream 
]
