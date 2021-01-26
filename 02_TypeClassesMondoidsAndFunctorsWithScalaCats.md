##Type Classes, Monoids, and Functors with Scala's Cats Library
Accompanying code can be found on [GitHub](https://github.com/dalgado-aws/ScalaCatsIntro)

### No Encapsulation in Functional Programming
In OOP, functions and data are bundled together in classes.

In Functional Programming, data and functions are kept separate.
And a multitude of programming techniques are available to create, combine, and edit functions.

We will study a use case of an "Order Processing System" to understand how the FP style of Type Classes 
varies from the traditional OOP style.

### OOP Style 
OOP can emulate the Functional Programming style of separating data and functions.

For e.g.  in an OOP Order Processing System, there could be an `Order` class with order information.
And, all functions that process Order objects could be kept in a separate `OrderProcessing` class.

Here is a  dummy implementation of such an approach:
It consists of 
- Data Definition
- Functions To Process The Data

#### Data For Order Processing
Accompanying code can be found on [GitHub](https://github.com/dalgado-aws/ScalaCatsIntro)
```
case class PlainOrder(val orderId:Int, 
                      val itemId:Int, 
                      val amount:Int)


// Specialized Order derived from PlainOrder
case class ExpressOrder(override val orderId:Int, 
                        override val itemId:Int, 
                        override val amount:Int, expressCharges:Int) 
    extends PlainOrder(orderId, itemId, amount)


// Order Container. 
//List is Co Variant so orders can be List[PlainOrder] or List[ExpressOrder]
class OrderBasket(val orders:List[PlainOrder]);


// Another Order class, but unrelated to the PlainOrder inheritance hierarchy
class UnrelatedMarsOder(info:String);
```

#### Functions For Order Processing
Accompanying code can be found on [GitHub](https://github.com/dalgado-aws/ScalaCatsIntro)

The order processing functionality can be enclosed in a class/object, keeping it separate from order data:

```
object Status {
  val Success = 1;
  val Failure = 0;
}

object OOOrderProcessor {

  def processOrder(plainOrder: PlainOrder) = Status.Success

  def processOrder(expressOrder: ExpressOrder) =  Status.Success

  def processOrderBasket(orderBasket: OrderBasket):List[Int]  =  orderBasket.orders.map(o => processOrder(o))

  def processUnrelatedMarsOrder(marsOder: UnrelatedMarsOder):Int = Status.Success
}
```
 
### Functional Style Using Type Classes
Lets see how we can use **Type Classes** to create an order processing system similar to the OOP one we defined above.

A `Type Class` defines some functionality just like an Interface in Java.

```
// This is a "Type Class"
trait OrderProcessor[A] {

  def processOrder(value:A) :Int

}
```

Members of the `Type Class` do not "implement" the `Type Class` Interface. 
Rather, to make `PlainOrder` a member of the `OrderProcessor` Type Class, 
`OrderProcessor[PlainOrder]` has to be defined.

_The reason each of the **instances**is marked `implicit` will become clear in later sections._

Accompanying code can be found on [GitHub](https://github.com/dalgado-aws/ScalaCatsIntro)
```
object OrderProcessorInstances {

  // adding PlainOrder to the OrderProcessor Type Class.
  implicit val plainOrderProcessor:OrderProcessor[PlainOrder] = (value: PlainOrder) => Status.Success

  // adding ExpressOrder to the OrderProcessor Type Class
  implicit val expressOrderProcessor:OrderProcessor[ExpressOrder] = (value: ExpressOrder) => Status.Success

  // adding List[PlainOrder] to the OrderProcessor Type Class
  implicit val orderBasketProcessor:OrderProcessor[List[PlainOrder]] = (orderBasket: List[PlainOrder]) => Status.Success

  // adding UnrelatedMarsOrder to the OrderProcessor Type Class
  implicit val marsOrderProcessor:OrderProcessor[UnrelatedMarsOder] = (value: UnrelatedMarsOder) => Status.Success

}
```
Then, the `Type Class` **instances** have to be "connected" to the Types. There are two ways of doing it
- Interface Objects
- Interface Syntax

#### Interface Objects
Interface Objects simply define a function with an **instance** as an implicit parameter.
```
object InterfaceObjectForOrderProcessing {

  def processOrder[A](a:A)(implicit orderProcessorInstance:OrderProcessor[A]) = orderProcessorInstance.processOrder(a)

}

```
When Interface Object functions are invoked, the **instances** have to be in scope.
```
object TestOrderProcessingTypeClass {

  import OrderProcessingInstances._

  val order = Order(1,2,3)

  InterfaceObjectForOrderProcessing.processOrder(order)
}
```

#### Interface Syntax
The second way to "connect" `Type Class` **instances** to Classes is by defining Interface Syntax
```
object InterfaceSyntaxForOrderProcessing {

    implicit class OrderProcessorImplicitClass[A](value:A) {

      def processOrder(implicit processr:OrderProcessor[A]) = processr.processOrder(value)

    }
}
```

The Interface Syntax invocation is more elegant than Interface Objects
```
object TestOrderProcessingTypeClassInterfaceSyntax {

  import OrderProcessingInstances._

  val order = Order(1,2,3)

  order.processOrder
}
```

We have seen how the syntax for OOP differs from that of FP.
At first glance, the `Type Class` syntax seems to be more onerous than the plain and straightforward OOP syntax. 

We must note that this syntax makes it possible to extend membership of the `Type Class` in ways that would 
not have been possible without this new syntax.

Consider a `Type Class` called `Russian`, with just one method `translateToRussian():String`

Ordinarily, we could not have been able to invoke "Hello Word".translateToRussian() on a `String` **instance** , 
but with the `Type Class` syntax we just discussed, it is possible to make that happen.
Similarly, there are libraries that add all kinds of additional functionality to existing Scala classes.

### [Cats](https://typelevel.org/cats/typeclasses.html) Is A `Type Class` Library 
We will take a look at the Cats Library. It is a collection of `Type Class` 
definitions and instances that work with most of the Scala Standard Library classes.

#### Adding Cats Dependency To sbt
The following dependency needs to to be added to the sbt build file to use Cats
```
libraryDependencies += "org.typelevel" %% "cats-core" % "2.0.0-M4"
```

#### Adding Cats Dependency To Scala REPL
To use Cats in the Scala REPL, create a file 'build.sbt', add the following 
```
name := "start_cats"
version := "0.1"
scalaVersion := "2.13.1"
libraryDependencies += "org.typelevel" %% "cats-core" % "2.0.0-M4"
```
Then, run sbt in the same directory
```
sbt
```
Once in sbt, type
```
console
import cats._
import cats.implicits._
1.show
```

Cats defines more than 25 [Type Classes](https://typelevel.org/cats/typeclasses.html)
A lot of functionality is available for application programmers.

Lets take a look at a few of the simple ones first:
- Show
- Eq

Later on, in this article, we can explore:
- Monoid
- Functor

A future post will be dedicated to :
- [Monad And Monad Transformers](03_MonadsAndMonadTransformersWithScalaCats.md)

### Show `Type Class`
Accompanying code can be found on [GitHub](https://github.com/dalgado-aws/ScalaCatsIntro)
The [Show](https://typelevel.org/cats/typeclasses/show.html) `Type Class` defines functionality similar 
to the toString() Object method in Java.
It is a good introduction to the `Type Classes` provided in the Cats Library.

The `Show` `Type Class`  defines a single function
```
trait Show[A] {

    def show(a: A): String
}
```
Let us see all the ways a Cats `Type Class` can be used in our application code.
Cats provides `Show` instances/implementation for many of the Scala Standard Library Classes.
```
  import cats._
  import cats.implicits._

  Option("thing").show
  "thing".show
  1.show
  33.33.show
  List(1,2,3).show
  Map(1->2, 3->4).show
```
All the above are using Interface Syntax.

Interface Definition can also be used 
```
    Show[Int].show(1)
    Show[Option[String]].show(Option("Hello"))
```
The `Show` **instance** for a custom class `Order` can be defined as 
```
  case class Order(id:Int, price:Int)

  import cats._
  import cats.implicits._

  implicit val orderShower:Show[Order] = (t: Order) => f"price is ${t.price} id is ${t.id}"
```
Above is the same as
```
  implicit val orderShower:Show[Order] = new Show[Order] {

      override def show(t: Order): String = f"price is ${t.price} id is ${t.id}"
  }
```
Then `show` can be invoked on  `Order` instances
```
  val newOrder = Order(id=1, price = 100)

  newOrder.show
```

A function that accepts any `Show` `Type Class` members can be defined as
```
  def processAnyShow[A](a:A)(implicit shower:Show[A]) = a.show

  processAnyShow(Option("thing"))
  processAnyShow("thing")
  processAnyShow(1)
  processAnyShow("33.33")
  processAnyShow(List(1,2,3))
  processAnyShow(Map(1->2, 3->4))
```
A function that accepts `Orders` that are `Show` `Type Class` members can be defined as
```
  def processOrdersHavingShow[A>:Order](order:A)(implicit shower:Show[A]) = f"${order.id} ${order.show}"
```

### Eq `Type Class` 
Accompanying code can be found on [GitHub](https://github.com/dalgado-aws/ScalaCatsIntro)
[Eq](https://typelevel.org/cats/typeclasses/eq.html) `Type Class` does type safe equality comparison.

Scala already has the `==` method. 
So, why does Cats library provide another `Type Class` for equality checking?

To examine some of the drawbacks of the `==` method, lets consider a code snippet.
Suppose we erroneously type in the following piece of code to filter out non 1 elements in a list.
We want our final list to only have `1`
```
  val allOnes = List(1, 1, 0, 1 ).filter(_ == "1") //bug in code ... should be 1, not "1"
                                                   //compiler will not detect error
```
Because of the bug in our code, `allOnes` will be an empty list. We expected to get List(1,1,1). 
The compiler did not warn us that we are comparing a String "1" with the Ints in the list.

If `Eq` `Type Class` was used instead, the compiler would detect the error
```
  import cats._
  import cats.implicits._

  List(1,2,3).filter(x => Eq[Int].eqv(x, "2")) //error caught. Using Interface Definition.
  List(1,2,3).filter(x => x === "2") //error caught. Using Interface Syntax.
```

Cats provides `Eq` **instances**for many of the Scala Standard Library Classes.
The negation of `===` is `=!=`

###  Monoid `Type Class`
Accompanying code can be found on [GitHub](https://github.com/dalgado-aws/ScalaCatsIntro)

In Discreet Maths, A Monoid consists of a Set, a Binary Operation, and an Identity element from the Set.
Two rules have to be satisfied:

- The result of the Binary Operation on any two elements of the Set should result in another element of the Set.

- And the Binary Operation applied to any element of the Set with the Identity element
 as the second operand should yield the the original element.

For e.g., Set of Integers, the operation of addition, and the identity element of 0 form a Monoid.
Adding any two integers yields another integer which satisfies the first rule,
 and adding an integer to the identity element of 0 yields the original integer which satisfies the second rule.

Similarly, the Set of Integers, the multiplication operation,and the identity element of 1 also forms a Monoid.

In Cats, the [Monoid](https://typelevel.org/cats/typeclasses/monoid.html) `Type Class` is defined as follows:
```
trait Semigroup[A] {
  def combine(x: A, y: A): A
}

trait Monoid[A] extends Semigroup[A] {
  def empty: A
}
```

Like for other Type Classes, Cats provides Monoid **instances** for many of the Scala Standard Library Classes.
```
  2 |+| 3  // Interface Syntax
  Monoid[Int].combine(2,3) //Interface Definition
  3 |+| 2 + Monoid[Int].empty // empty is the Identity Element
  Option(2) |+| Option(3) |+| Option(6)
  Map(1->2) |+| Map(2->3) |+| Map.empty
  List(1,2,3) |+| List(4,5,6) |+| List(7)
```

`|+|` is the Interface Syntax for Monoid.

The **instance** provided by Cats is quite useful in many daily programming tasks.
For e.g. a List of Maps could be combined like below
```
  val listOfMaps = List(Map(1->1, 2->2), Map(3->3, 4->4), Map(5->5)
  listOfMaps.reduce( _ |+| _)
```

### `Type Classes` For Generics
Before we discuss the next `Type Class` , it would be helpful to have a short discussion about Generics.
Generics are classes that take a Type parameters. 
Most of us are familiar with the Java and Scala collection classes.
Collection classes mostly employ Generics as Containers. However, as we will see later in this post, 
there are other ways in which Generics can be used.

###`Producer` And `Consumer Methods` In Generics
The methods in a Generic class can be classified as:
- `Consumer Methods`:  Methods that have a parameter of Type T ... methods that consume T
- `Producer Method`s: Methods that return **instances** of Type T ... methods that produce T
This classification is critical for understanding of the next type class: Functor

### Generic As Containers
We usually think of Generics as Containers. For e.g. List[T], and Array[T] are Generics that are Containers
In general, Containers of Type T store data of type T and have methods to return stored data.
for e.g.
```
class Container[+A](val item:A)
```
The reason for use `+A` instead of just `A` will become clear later in this section.
Also note taht the parameter is a `val`, not a `var`.

####  Containers Are Covariant(+)
It makes sense for Containers to be Covariant. i.e. A `Container[Apple]` should be treated as `Container[Fruit]`.
Any instance of `Container[Fruit]` should be replaceable by an instance of `Container[Apple]`.
This feature wherein `Container[A]` is a subclass of `Container[B]` if A is a subclass of B is called `Covariance`
We defined `Conatiner[+A]` with the `+` sign to indicate covariance.
Lets take a look at some code to see how this works.
```
  class Fruit

  class Apple extends Fruit

  // this is allowed because Container is covariant i.e. it is defined as Conatiner[+A]
  val appleContainer:Container[Apple] = new Container[Apple](new Apple())
  val fruitContainer:Container[Fruit] = appleContainer
```

The `fruitContainer` now points to an  `appleContainer`.
This is fine since both `appleContainer` and `fruitContaier` can **produce** `Fruit`.

>> Can we put a `Fruit` in the `fruitContainer`?
Suppose we had such a `Consumer Method` defined on `Container`:
```
def put(newItem:A) {item = newItem}
```
 then the following invocation would result in puttting a `Fruit` in an `Apple` container because
 `fruitContainer` actually points to an `appleContainer`
```
    fruitContainer.put(new Fruit()) // trying to change appleContainer item to Fruit
```
and this would corrupt the `appleContainer`.
If we then called `get()` on the `appleContainer`, it would return a `Fruit`, not `Apple`.

Fortunately,`Consumer Methods` are not allowed on types that are declared as Covariant(+A).
Only `Producer Methods` are allowed.
So Covariant Types work well with the inheritance hierarchy but do not allow`Consumer Methods`.

#### Covariant Functors
Say we have a `Container[Apple]` and we want `Container[AppleSauce]`.

To convert  `Container[Apple]` to  `Container[AppleSauce]`, 
all we need is a function that converts `Apple` to `AppleSauce` i.e. `MappingFunction:Apple=>AppleSauce`

This seems obvious! However, the above statement cannot be generalized to all Generic Types.
It is only applicable to Generics that are Covariant.

In general, if we have any Covariant Type `F[+A]` and a function `f:A=>B`, we can create `F[B]`

Let us see how we can define a method to convert `F[A]` to `F[B]` given a function  `f:A=>B`:
```
abstract class CovariantType[+A]() { self =>

  def someProducerMethod:A

  def changeContainerAtoContainerB[B](f:A=>B): CovariantType[B] =  new CovariantType[B] {

    override def som`Producer`Method: B = f(self.someProducerMethod)
  }

}
```
The utility method `changeContainerAtoContainerB`, that takes in `f:A=>B` and returns `F[B]` is usually called `map`.
All it has to do is subclass the Container and enclose any original `Producer Method`s within `f`

The Container Type together with the Function forms Covariant Functor.
The [Functor](https://typelevel.org/cats/typeclasses/functor.html) `Type Class` is defined for Generics.

#### Why `Consumer Methods` Will Not Work
If the Container type had a `Consumer Method`, the above strategy of subclassing(anonymous subclassing) the Container would not work.
We will not be able to define new `CovariantType[B]` using methods of `CovariantType[A]` like we did above.

The `Consumer Methods` in `new CovariantType[B]` would need to process process/consume a `B` instance.
Could we somehow  use the `Consumer Method` definition in `CovariantType[A]` 
to redefine the same `Consumer Method` for `CovariantType[B]` like we did for the `Producer Methods`?

No. The `Container[A]` `Consumer Method` processes an `A` instance.

And the subclassed `Container[B]` `Consumer Method` would need to consume/process a `B` instance.

What we would need is a function that converts B to A. 

What we have is a function that converts A to B.

#### Why Do We Care About Covariant Functors
Covariant Functors allow us to compose and build chains 
```
List(1,2,3).map(function1).map(function2).map(function3)
```
Without the `map` method, the same code would have to be written as
```
    val originalList = List(1,2,3)
    val firstChange =  firstMap(originalList)
    val secondChange = secondMap(firstChange)
    val result = thirdMap(secondChange)
```
There is a important case that we have not yet considered while chaining the `map` calls.
Is the `map` allowed to fail? 

Consider the following code snippet:
```
Container("1").map(convertStringToInt).map(convertIntToRoman)
Container("i").map(convertStringToInt).map(convertIntToRoman)
```
The second chain has a problem. 
What should `convertStringToInt` do when supplied with an illegal value `i`?

One solution would be to just throw an Exception.

Or maybe the it should return some kind of error code.

The `Functor` pattern does not have the ability to handle intermediate errors in a chain.
We will have use a slightly different pattern. Mondad.
We will examine Mondad in the next post.

### Contravariant Functors
In the last section we saw how Generics of Type `A` could be used as Containers of Type `A`. 
And it makes sense to make them Covariant.

There is another way we could use Generic Types: A Generic of Type T 
may be thought of as a  **Service Provider** or **Processor** of Type `T`. 

Consider the following snippet:
```
class SweetnessChecker[-A]() {
    def isSweet(a:A):Boolean = False;
}
```
`SweetnessChecker[Apple]` is not a Container. It does not store any value.
It **processes** or is a **ServiceProvider** for the `Apple` Type.

#### Service Types Are Contravariant
Suppose, we have a hierarchy of classes  Green Apple < Apple < Fruit and function that process Type `Apple`:
```
def checkApple(apple:Apple):Boolean = {
    val sweetnessChecker = new SweetnessChecker[Apple]();
    return sweetnessChecker.isSweet(apple)
}

```
In the function `checkApple`, could we change 
```
  val sweetnessChecker = new SweetnessChecker[Apple]();
```
to
```
  val sweetnessChecker = new SweetnessChecker[GreenApple]` 
```
No.
Because `SweetnessChecker[GreenApple].isSweet()` takes in `GreenApple`.
Our function `checkApple` has an ordinary `Apple`.

But we can change it to 
```
 val sweetnessChecker = new SweetnessChecker[Fruit]()
```
That is `Fruit.isSweet(Fruit)` takes in a `Fruit` and we can pass in the `Apple` that we have.

This seems counter intuitive at first: The `SweetnessChecker[Fruit]` seems to be subclass of `SweetnessChecker[Apple]` even though 
`Apple` is a subclass of `Fruit`.

Service Types have `Consumer Methods` and Types with `Consumer Methods` are Contravariant.

#### Contravariant Functors
Contravariant Types also have an interesting property. 

If we have a contravariant  type `F[A]` and a function `Z => A` then we can create type `F[Z]`

Say we have Covariant Type `SweetnessChecker[Apple]`
```
class SweetnessChecker[Apple]() {
    def isSweet(a:Apple):Boolean = False;
}
```
and a Function  which converts `Fruit` to `Apple`
```
    def fruitToAppleConverter(fruit:Fruit):Apple = new Apple()
```
then we can have create Type `SweetnessChecker[Fruit]`
```

class SweetnessChecker[Fruit] () {
    def isSweet(f:Fruit):Boolean = new SweetnessChecker[Apple]().isSweet(fruitToApple(f)))
}
```
This Generic Type along with the converter function forms a Contravariant Functor

The utility function that applies the converter function is usually called `contramap`

How would we define `contramap`?
```

abstract class SweetnessChecker[-A]() { self=>
  def isSweet(a: A): Boolean

  def contramap[Z](f:Z=>A) = new SweetnessChecker[Z] {
    override def isSweet(z: Z): Boolean = self.isSweet(f(z))
  }
}
```
Can we figure out why `Producer Method`s cannot be supported by Contravariant Functors?
Take a look how the `Producer Method`s are handled in the `map` definition of `Container` class.

### Why Do We Care About Contravariant Functors?
Just like Covariant Functors, Contravariant Functors allow us to compose and build chains, by prepending functions:
```
SweetnessChecker[Apple].contramap(fruitToApple).contraMap(eatableToFruit).isSweet(eatable)
```
The first `contramap()` yields `SweetnessChecker[Fruit]`, and the second `contramap` converts `SweetnessChecker[Fruit]` to `SweetnessChecker[Eatable]` 
The conversions are happening in reverse() order of the inheritance hierarchy.

### Invariant Functors
- Covariant Types can have `Producer`s but no `Consumers`
- Contravariant Types can have `Consumer`s but no `Producers`

If a Generic Type has `Producer` as well as`Consumer Methods`,it is Invariant ...neither Covariant nor Contravariant.
Suppose we have a Generic Type `F[A]` with both `Producer`s and `Consumer`s.
How can we convert it to `F[B]` using the strategy of anonymous subclassing that we used for Covariant and Contravariant Functors?

`F[A]` will have `Producers`. i.e. methods that return `A`. 
We will need to somehow modify these methods to return `B` instead.
So we will need a function to convert `A=>B`

`F[A]` will have`Consumer`s i.e. methods that consume `A`.
We will need to somehow modify these methods to accept `B` instead.
Se we need a function that will convert `B=>A` and feed it to the `Consumer` methods.

So, in order to convert `F[A]` to `F[B]`  we will need two functions: `A=>B` and `B=>A`

Consider a class that has `Producer` and`Consumer Methods`.
Lets try to creat an `imap` method to convent a Generic Type with `Producers` and `Consumers` from `A` to `B`:
```
abstract class DollarConverterFor[A] { self =>

  /`Consumer Method` consumes A
  def toDollar(v:A):Double


  /`Producer Method` produces A
  def fromDollar(y:Double):A


  def imap[B](f:A=>B)(g:B=>A):DollarConverterFor[B] = new DollarConverterFor[B] {

    // Use B=>A and invoke the toDollar() method from Dollar[A]
    override def toDollar(v: B): Double = self.toDollar(g(v))
    // same as contramap

    // Use A=>B to convert the result of the method from Dollar[A]
    override def fromDollar(y: Double): B =  f(self.fromDollar(y))
    // same as map
  }
}
```
The Generic Type along with the two functions form an Invariant functor.

#### Why Do We Care About Invariant Functors
Invariant Functors allow chaining in both directions.
Consider the following code:
```
case class Euro(euroValue:Double)

case class Yen(yenValue:Double)

case class Pound(poundValue:Double)

val euroToPound = (e:Euro) => Pound(e.euroValue/2)   // A => B

val poundToEuro = (p:Pound) => Euro(p.poundValue *2) // B => A

val euroAndDollar =  new DollarConverterFor[Euro] () {

  override def toDollar(v: Euro): Double = v.euroValue/0.75

  override def fromDollar(y: Double): Euro = new Euro(y * 0.75)
}

//chaining forward
val euroAndPound = euroAndDollar.imap(euroToPound)(poundToEuro)
euroAndPound.toDollar(Pound(33))

chaining backward
val anotherEuroAndDollar = euroAndPound.imap(poundToEuro)(euroToPound)
euroAndDollar.toDollar(Euro(33))

```
We have `DollarConveterTo[Euro]`. How can we get `DollarConverterTo[Pound]`?
All we need is `Euro=>Poung` and `Pound=>Euro`


####Summary For Generic Types And Functors
Restriction | Gain | Use | Functor | Functor Use
---|---|---|---|---
Only`Producer Method`s,`Consumer Methods` Not Allowed | Covariance                                 | Containers                    |Forms a Functor with A=>B                | Chaining
Only`Consumer Methods`,`Producer Method`s Not Allowed | Contravariance                             | Service Types or Processors   |Forms a Functor with B=>A                | Chaining
No Covariance or Contravariance                     | Can have`Producer` and`Consumer Methods`     |                               |Forms a Functor with A=>B and B=>A       | Chaining
 
 
### Functors in Cats
We have see that a `Type Class` is just like an interface.
For e.g. the `Type Class` `Show` is defined as 
```
trait Show[A] {
     def show(a:A):String
}
```
How would we define a `Type Class` on a Generic Type?
A Functor `Type Class` would need to have a `map` method which converts the Generic Type from `A` to `B` using a function `A=>b`
If we look at the definition in Cats, we see the following:
```
trait CovariantFunctor[F[_]] {
  
  def map[A, B](gt:F[A], F:A=>B):F[B]
 
}
```
The `F[_]` indicates that this `Type Class` is for Generic Types that has a single Type Parameter.
And there is a `map` method that processes generic type `F[A]`, and a function `A=>B` to return `F[B]`.

As usual Cats defines Covariant functors for many of the Covariant Types in the Scala Standard Library.
Many of the Scala Standard Library Classes already have a `map` method, so the `instances` provided by Cats is redundant.

Below code snipped shows how we can make our `Container` class a member of the `Functor` `Type Class`
```
import cats._

implicit val functorInstanceForContainer = new cats.Functor[Container] {

  override def map[A, B](fa: Container[A])(f: A => B): Container[B] =  new Container[B](f(fa.item))
}
```

A meta use case would be to define a function that works with all "mappable" Classes
```
  import cats.implicits._;

  def changeContainer[F[_], A](container:F[A])(implicit functor:cats.Functor[F])  = container.map(x=>1)
```

We can then invoke the function for which  `Functor` instances are defined

```
  changeContainer(Option("hello"))
  changeContainer(List(1,2,3))
  changeContainer(new Container("hello"))
```

### Conclusion
The cats(short for Categories) library provides a lot of functionality that can make our Scala Code better.
It is worth while to spend time and get to know the various `Type Classes` and **instances** that have been made
available to us.

### References
[Scala With Cats](https://underscore.io/books/scala-with-cats/) by Noel Welsh and Dave Gurnell
