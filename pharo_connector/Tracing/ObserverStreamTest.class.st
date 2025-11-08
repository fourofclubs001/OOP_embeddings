Class {
	#name : 'ObserverStreamTest',
	#superclass : 'TestCase',
	#instVars : [
		'instVarOne'
	],
	#category : 'Tracing',
	#package : 'Tracing'
}

{ #category : 'auxiliar' }
ObserverStreamTest >> assignCollectionWithInstanceVariable: number [
	
	|tmp |
	instVarOne := OrderedCollection new.
	instVarOne add: number.
tmp :=OrderedCollection new add: instVarOne.
^tmp
]

{ #category : 'auxiliar' }
ObserverStreamTest >> assignCollectionWithTemp: number [
	
	|tmp|
	OrderedCollection new add: number.
tmp :=OrderedCollection new add: OrderedCollection new.
^tmp
]

{ #category : 'auxiliar' }
ObserverStreamTest >> assignCollectionWithTwoTemp: number [
	
	|tmp tmp2|
	tmp2 := OrderedCollection new add: number.
tmp :=OrderedCollection new add:tmp2.
^tmp
]

{ #category : 'tests' }
ObserverStreamTest >> test01TempVariableAssignmentIsRegistered [

	|contextRecorder observer|
	
	contextRecorder := ContextRecordedDecorator with: thisContext.
	observer := ObserverStream new.
	
	contextRecorder addObserver: observer .
	contextRecorder runSimulated: [ self assignCollectionWithTemp: 1 ].
	
	self assert: (observer record anySatisfy: [ :register | register includesSubstring: 'tmp :='  ])
	
	
	
]

{ #category : 'tests' }
ObserverStreamTest >> test02SendIsRegistered [

	|contextRecorder observer|
	
	contextRecorder := ContextRecordedDecorator with: thisContext.
	observer := ObserverStream new.
	
	contextRecorder addObserver: observer .
	contextRecorder runSimulated: [ self assignCollectionWithTemp: 1 ].
	
	self assert: (observer record anySatisfy: [ :register | register includesSubstring: 'add:'  ])
	
	
	
]

{ #category : 'tests' }
ObserverStreamTest >> test03SendWithTwoTempsCorrectlyRegistered [

	|contextRecorder observer|
	
	contextRecorder := ContextRecordedDecorator with: thisContext.
	observer := ObserverStream new.
	
	contextRecorder addObserver: observer .
	contextRecorder runSimulated: [ self assignCollectionWithTwoTemp: 1 ].
	
	self assert: (observer record anySatisfy: [ :register | register includesSubstring: 'add:'  ]).
	self assert: (observer record anySatisfy: [ :register | register includesSubstring: 'tmp :='  ]).
	self assert: (observer record anySatisfy: [ :register | register includesSubstring: 'tmp2 :='  ])
	
	
	
]

{ #category : 'tests' }
ObserverStreamTest >> test04OperatingInstanceVariable [

	|contextRecorder observer|
	
	contextRecorder := ContextRecordedDecorator with: thisContext.
	observer := ObserverStream new.
	
	contextRecorder addObserver: observer .
	contextRecorder runSimulated: [ self assignCollectionWithInstanceVariable: 1 ].
	
	self assert: (observer record anySatisfy: [ :register | register includesSubstring: 'instVarOne :='  ]).
	self assert: (observer record anySatisfy: [ :register | register includesSubstring: 'tmp :='  ]).
	
	
	
]
