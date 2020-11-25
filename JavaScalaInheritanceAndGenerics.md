## Generics and Polymorphism in Java and Scala

###  Extensible Programming With Polymorphism
As programmers, we strive to write extensible code.

Adding new features should be easy.
Modifying existing behaviour should be easier.

As OO Programmers, we have 2 main tools to write extensible and maintainable programs:

- [x] **Enacpsulation** Bundling data and methods together
- [x] **Polymorphism** Extending program behaviour with Specialized Sub Classes

In OOP, Specialized Sub Classes are plugged into polymorphic functions to extend program behaviour.
How this core facility of Polymorphism is affected by Generics is the study of this article.

We can summarize the core polymorphic function design pattern as follows:

We design the program using polymorphic function:
```
interface Engine {
     int  start()
     int stop() 
}

// this functionality is pluggable, extensible
class DieselEngine implements Engine {

 //first Specialiasation of Engine
     //implement start() and stop() methods
}

public class Main {

    // a polymorphic function to extend functionality
    void polymorphicFuction(Engine someEngine) {

        someEngine.start();
        someEngine.stop();
    }

    public static void main(String [] args) {

        Engine engine = PetrolEngine();
        polymorphicFunction(engine);
    }

}
```
Then, to extend this program, we just need create another Engine Specialization
```
class PetrolEngine implements Engine {
    //Another Specialzation of Engine
    //implement start() and stop() methods
}

public class Main {

    void polymorphicFuction(Engine someEngine) {
        someEngine.start();
        someEngine.stop();
    }

    public static void main(String [] args) {
        // invoke the polymorphic function with the new specialization
        Engine anotherEngine = new DieselEngine();
        polymorphicFunction(anotherEngine);
    }
```

To develop a comprehensive understanding of Generics and its interplay with Polymorphism we will 
visualize Generics as Containers with methods that are **Producers** and/or **Consumers**.

### Generics/Containers as another form of Specialisation Management
Polymorphism allows us to handle specialization or modification gracefully.
Generics can also be viewed as another form of Specialisation Management. 
for e.g. List\<String\> and List\<Int\> are specialised forms of List\<T\>

The Specialisation Management provided by Generics makes casting redundant and code Type Safe.

So we have two forms of Specialisation Management:
- Sub Class based Specialisation and 
- Generics based Specialisation.

It will be interesting to see how these two forms of specialisation interact.

### Producer and Consumer Methods
Let s take a look at a Generic class
```
class Container<T> {

    private T instance; 

    public T get() {
        return instance;
    }

    public void put(T newInstance) {
        this.instance =  newInstance;
    }
}

```

It is helpful to think of a Generic Class of Type T as a **Container** with 3 types of components:
- [ ] Instances of the Type for e.g. `private T instance`
- [ ] Methods that return Type instances for e.g. `public T get()`. These are **Producer Methods**.
- [ ] Methods that accept Type instance as parameter for e.g. `public void put(T newInstance)`. These are **Consumer Methods**.

A method could be Producer and Consumer at the same time.
A Generic Class may have many other types of methods and instances but for the purpose of our discussion
here , these are the 3 main components to consider.

**Producer** methods can also be thought of as **Reader** methods.

**Consumer** methods can also be thought of as **Writer** methods.

### Generics/Containers And Polymorphism
How do the two features interplay? Is polymorphism enhanced with the addition of generics?
What are the potential pitfalls when combining these two features?

### Producer Methods In Polymorphic Functions
If there is an inheritance relationship between classes, it would be intuitive to have the same relationships 
between containers of those classes

Say we have an inheritance hierarchy `Organism` `<` `Animal` `<` `Dog` `<` `Husky`

It would be great to have `Container<Organism>` `<`  `Container<Animal>` `<` `Container<Dog>` `<` `Container<Husky>`

Then, we could create a polymorphic function such as:
```

public void processMyPolymorphicContainer(Container<Animal> animalContainer) {
    Animal animalFromContainer = animalContainer.get();
    animalFromContainer.animalMethod();
}
```
This method can be passed an instance of either `Container<Animal>`, or `Container<Dog>`,
 or  `Container<Husky>`
 
The get() methods on each of these containers will yield `animal`, `dog`, or `husky`. 
Each of these is a `dog`, so we can always call `animalMethod()` on these instances.
Everything seems to be working nicely and as expected.

>The main take away from the analysis till now is that Producer Methods on a Container work as 
expected with the inheritance hierarchy

Note that there is a qualifier that we used: `Producer Methods`. 

Not all methods! Only **Producer Methods** work as expected with the inheritance hierarchy!

### Consumer Methods In Polymorphic Functions
Let us experiment with Consumer Methods in Polymorphic Functions. 
Remember, Consumer Methods are those that take a Type instance as parameter.

```
public void processMyPolymorphicContainer(Container<Animal> animalContainer) {
                     animalContainer.put(new Animal())
}
```
The only thing this method does is store an `animal` in the animalContainer passed in as parameter.
Let us check what containers are possible candidates to be passed to this Polymorphic Function:
We could call:
- processMyPolymorphicContainer(animalContainer)
- processMyPolymorphicContainer(dogContainer)
- processMyPolymorphicContainer(huskyContainer)

The first call is fine. 
processMyPolymorphicContainer() method will save an Animal instance  in the animalContainer.
The second and third invocations are a problematic.
They will cause an animal to be stored in a dogContainer or a huskyContainer.

Later on if we do a dogContainer.get() on the same container, we will get an `animal` from dogContainer. 
And if we do  `dogContainer.get().dogMethod()`, the get() would have returned a `animal` instead of a `dog`
And calling a `dogMethod()` on an `animal` instance is obviously not right.

>So, we see that unlike a Container's Producer Methods, calling a Container's Consumer methods 
in a polymorphic function does not work well.
Consumer Methods have the ability to corrupt instance variables if used inappropriately in Polymorphic Functions.

Let us see what happens if we pass containers with super classes of Animal to our Polymorphic Function.

- processMyPolymorphicContainer(organismContainer)

The function will store an `animal` in the organism Container.
This is fine since `animal` is an `organism` 
If we then call the `get` method on the `organismContainer`, it will return an `animal` which is fine.
An `animal` is an `organism` for all intents and purposes.

>The very interesting and unintuitive learning from our experiment is that we can pass containers with
super class of Type T to a polymorphic function that invokes the Container's consumer function.

### Java Notation 
Java has a notation to tell the compiler that a polymorphic function will only invoke Producer Methods on the Container parameter.
 ``` 
void myPolymorphicFunction(Conatiner<? extends Animal> p) {
     //can call producer methods on container p
} 
```
In return, the compiler will allow the function to be invoked with Container\<Animal\>, Container\<Dog\> , 
or Container\<Husky\> i.e. Containers having Animal and its subclasses.
 
What about Consumer Methods on Container classes? 
A function can be annotated as 
 ``` 
void myPolymorphicFunction(Container<? super Animal> p) {
    //can call consumer methods on container p
 }
```
 , then the function is allowed to invoke only Consumer Methods on the Container and the function can be invoked
 on Containers bearing Animal and its superclasses(Organism)
 
 If a function wants to invoke Producer as well as Consumer Methods on the container, then the function
 cannot be invoked with Containers bearing super or sub classes.

### Scala
In scala, a Container itself has to decide whether it is going to have Producer or Consumer Methods. 
And, unlike Java, there is no special annotation for polymorphic functions.

A Container can have Producer Methods if it is defined as
```
class Container[+A](val instance:A)
```
And a Container based polymorphic function defined as below with no special annotation  
```
def processMyPolymorphicContainer( animalContainer:Container[Animal])
```
will accept instances of Container[Animal], and Container[Dog], and Container[Husky] 
since since Husky and Dog are subclasses of Animal

Similarly, A Container can have Consumer Methods if it is defined as
```
class Container[-A]()
```
And a Container based polymorphic function defined as below with no special annotation
```
def processMyPolymorphicContainer( animalContainer:Container[Animal])
```
will accept instances of Container[Animal], and Container[Organism]
since Organism is a superclass of Animal

### A Special Case
>A Container declared as a Producer can have a Consumer Method if the Method Parameter Type 
is a superclass of the Container Type.

for e.g. a Producer[Dog] can have a Consumer Method with param **(Animal a)** since Animal is a super type of Dog.

Such a method will never be able to corrupt Container[Dog] because it can never 
assign the method parameter instance of Type Animal to the Dog Instance that is stored in the Container.

Let us see how these kinds of methods can be put to use.
Consider this code snippet:
```
// A Container defined as a Producer 
class ContainerOfPairs[+A](first:A, second:A) {

    // A Consumer Method with restrictions on the Parameter Type. 
    //It has to be super type of the Container Type
    def changeFirst[B>:A](to:B): ContainerOfPairs[B] = {
      new ContainerOfPairs(to, second):ContainerOfPairs[B]
    }
}
```

The `changeFirst[B>:A](to:B)` is a Consumer Method in a class that is defined as a Producer
The method only accepts a superclass of the Container Type. 
It then returns a new Container of type B. 

The existing Container is not modified. 
A new Container has been created instead.
This is a standard pattern we see in may places in the Scala Lib.
```
  val numberList = 1::2::3::Nil
  val stringList = "a"::"b"::"c"::Nil
  val combined:List[Any] = numberList:::stringList
```

`numberList` is `List[Int]`, and `stringList` second is `List[String]`
The `:::` method is defined as `def :::[B >: A](prefix : scala.collection.immutable.List[B])`

Why is the method returning instance of `List[Any]`?

It is invoked on `List[String]` and the parameter is of type `List[Int]`.
`Int` is not super type of `String` , but `Int` is sub type of `Any` and `Any` is super type of `String`.
So an `List[Any]` is returned.

### Function Is A Container That Consumes Type A And Produces Type B
We can think of Function/Methods as Containers with Producer and Consumer Methods.

Consider the following code snippet:

Any function can be thought of as a Container that consumes a Parameter of Type P and returns 
a value of type R.
```
class FunctioonAsContainer[-ParamType, +ReturnType] {
   def apply(param:ParamType):ReturnType  = throw new Exception("Not implemented!")
}
```
Then we can have Container based polymorphic functions that take in function containers:
```
object HelloWorld {

    var intToInt = new FunctionAsContainer[Int,Int]();
    var anyToNothing = new FunctionAsContainer[Any, Nothing]()

    def processPolymorphicContainer(fn:FunctionAsContainer[Int, Int]): Unit = { }

    def main(args: Array[String]) {
        processPolymorphicContainer(intToInt);
        processPolymorphicContainer(anyToNothing);
    }
}
```

The `processPolymorphicContainer` function requires an `Int` to `Int` function. i.e. a function that consumes `Int` and produces `Int`
Since `Any` is a super class of `Int`, the `Int` consumer can be replaced by an `Any` consumer.
And since `Nothing` is a sub class of `Int`, the  `Int` producer can be replaced by a `Nothing` producer.

## Conclusion
We can build a comprehensive understanding of Generics and Polymorphism if we think of Generics as Containers with 
Producer and Consumer functions.

Containers that are Producers work well with the regular inheritance hierarchy. They are Co Variant.
Containers that are Consumers work with the hierarchy in **reverse** order. They are Contra Variant.
Containers that are neither Producers not Consumers do not work with the inheritance hierarchy at all.
They are Invariant.

## References
[Covariance and contravariance in Scala](http://blog.kamkor.me/Covariance-And-Contravariance-In-Scala/)











