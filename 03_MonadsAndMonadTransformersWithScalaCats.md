### Monads And Monad Transformers With Scala's Cats Library


### What is a Monad?
Monad is a "functional design pattern" that allows "chaining" of operations.
Functor is similar design pattern that does something similar.
I have covered [Functors in an earlier post](02_TypeClassesMondoidsAndFunctorsWithScalaCats.md).
In this post we will emphasize the "chaining" aspect of Monads. 
We will also avoid the the use of "for comprehension" syntax so as to highlight how the Monad design pattern 
supports chaining in various circumstances. i.e. error handling while chaining(Option, Either), 
passing "global" information to components of the chain (State), logging each of the components in the chain (Writer),
etc.


### Function Composition/Chaining

Consider the following 3 functions.
```
  def removeWhitespace(str:String):String= str.trim

  //Given a string in yyyy/mm/dd format, return the year as int
  def extractYear(str:String):Int = Integer.parseInt(str.split("/")(0))

  def olderThan18(birthYear:Int):Boolean = java.time.Year.now.getValue - birthYear >= 18
```
The functions could be composed/chained as follows
```
    def eligibleToVote(str:String) = olderThan18(extractYearFromDateString(removeWhitespace(str)))
```
or
```
    def eligibleToVote(str:String) = removeWhiteSpace andThen extractYeareFromDateString andThen olderThan18 
```
or
```
   def eligibleTovote(str:String) = olderThan18 compose extractYearFromDateString compose removeWhiteSpace
```
Another way is to use `map` from a Functor
```
  def eligibleToVote(dateString:String):Boolean = Option(dateString).
    map(removeWhitespace).
    map(extractYear).
    map(olderThan18).get
```
We could have used a `List` instead of an `Option`:
```
  def eligibleToVote(dateString:String):Boolean = List(dateString).
    map(removeWhitespace).
    map(extractYear).
    map(olderThan18)(0)
```
And finally, the composition can be invoked as follows: 
```
  val result = eligibleToVote("2222/11/22")
```
>>There is one issue that we have not discussed yet. How are errors handled? If one of the intermediate functions in the 
chain is not able to process its data, how should it behave?
Consider the following invocation of our composition:
```
     val result = eligibleToVote("/11/22")
```
We know that `extractYearFromDateString` will not be able to successfully produce a valid output.
`Integer.parseInt` will throw an NumberFormatException!
>Is there a better way to handle errors in the chain?

One option would be for the function to return some error code.

Suppose `exractYearFromDateString(str:String)` returns an error code, say `-1`. 
The function that receives the code (`olderThan18()`) will need to handle this special input.

>For some functions , it might not even be possible to return an error code at all!
>
For e.g., consider a function `def parseInt(str:String):Int`. 
Such a function has no valid  `Int` error code.
Let us see how this is resolved in a much better way by using the Monad Design Pattern.

### The Monad Design Pattern
Monads is a design pattern that allows chaining of functions.
Of the many benefits that are made available by the Monad Design Pattern, 
we will analyse the chaining with error handling feature first.
Later on, we will see that the same design pattern can be molded in many ways to provide dependency injection,
state management, logging in a multi threaded environment, and much more.

We saw how Functor(i.e. map()) can be used to chain functions. 
With Monads the chaining has a slightly different syntax.

In order to use the Monad design pattern, some adjustments have to be made to our code.
A function in the chain that earlier returned `Int` will now have to return `Option[Int]`.
To indicate an error condition, the return values will be `None`.
We are using `Option` Monad for out analysis. 

If we want to use `List` instead, then our function will have to return `List[Int]` on success, and `Nil` on failure.

Let us take a look at how the code will have to be adapted.
```
  def removeWhitespace(dateString:String):Option[String]= ???

  //* Given a string in yyyy/mm/dd format, return the year as int
  def extractYearFromDateString(str:String):Option[Int] =  {
    if (true) //if we are able to extract year successfully, we will return Option(yearInt)
      Option(2001)
    else
      None // Error condition. None is a subclass of Option
  }

  def olderThan18(year:Int):Option[Boolean] = java.time.Year.now().getValue - year

```
The functions are chained with `flatMap()`
```
  def birthYearAfter2000(dateString:Option[String]):Boolean = dateString.
    flatMap(removeWhitespace).
    flatMap(extractYearFromDateString).
    flatMap(olderThan18).get
```

Lets go through all the changes that were made to our code.
- An `Option` is being used. `Option` is just a Container. We could have used `List` instead, or any other [Covariant Generic Container](02_TypeClassesMondoidsAndFunctorsWithScalaCats.md).
- Every function that earlier returned Type `A` has been modified to return `Option[A]`
- On success, the function returns `Option[A]`, on failure it returns `None`. `None` is a subclass of `Option`. This is very important to note.
- Calls to `map` have been replaced by calls to `flatMap`

`None` is the error code that is passed along the chain. If any of the functions in the chain fail, we will get a `None` else
we will get a `Option[A]` with the final result.
It will be interesting to see how and why `flatMap()` works!


### Implementing A Container With flatMap()

[github link](https://github.com/dalgado-aws/ScalaCatsIntro/blob/main/src/main/scala/toppackage/g_MonadFlavours_0_Option.scala#L67)

In the above example, we used the `Option` Monad.

>We will try to define a homegrown Monad from scratch that will allow us to chain functions and handle errors gracefully.


First, we define the most basic Generic Container with the `flatMap` method:
If the `+A` is making you squeamish, please read my earlier post 
on [Generics](01_JavaScalaInheritanceAndGenerics.md) to understand why we use `+A` instead of just `A`.
```
  trait Container[+A] {

    def flatMap[B](f:A=>Container[B]):Container[B]
  }

```
Note that the `flatMap` method returns `Container[B]`. 
Any class that has a method with a signature similar to `flatMap` is a Monad.
Let us see how we can implement this method to provide chaining along with graceful handling of intermediate errors.
The chained functions can have 2 possible return values.
- On success, the function returns a Container subclass with the computed value
```
  class GoodContainer[+A](val data:A) extends Container[A] {

    override def flatMap[B](f:A=>Container[B]):Container[B] = f(data)

  }
```
- and on failure, function returns another subclass of Container. Let us call it `ErrorContainer`
```
  class ErrorContainer[+A] extends Container[A] {

    override def flatMap[B](f: A => Container[B]): Container[B] = new ErrorContainer[B]

  }
```
Lets discuss the `flatMap` implementation in both the sub classes of `Container`.

Actually, the `flatMap` of the `ErrorContainer` is more interesting.
It does not do anything with the supplied function `f`!
This is because once an error is generated in a function chain, the rest of the chain just propagates the error.

The `flatMap` in the `GoodContainer` actually applied the function.
The application can result in another `GoodContainer` or an `ErrorContainer`
And the next function in the chain will be invoked on this `GoodContainer` via its `flatMap` method.


The chains can be built as below:
```
  val success = true

  def chainable1(i:Int):Container[Int] = if(success) new GoodContainer(100) else new ErrorContainer

  def chainable2(i:Int):Container[Int] = if(success) new GoodContainer(100) else new ErrorContainer

  val resultOfChaining:Int = new GoodContainer(1).flatMap(chainable1).flatMap(chainable2).getOr(3)
```
The 'resultOfChaining' can either be a `GoodContainer` or an `ErrorContainer`
It makes sense to add a `getOr` method to `Container` to retrieve the final value from the chain! 
```
    def getOr[B>:A](v: B): B = ???
```
Again, if the `B>:A` notation is not familiar,
 I would suggest going through an earlier post on [Generics](01_JavaScalaInheritanceAndGenerics.md)


### Monads in Cats

In Cats, the Monad Type Class is declared as follows:
```
trait Monad[F[_]] {

  def pure[A](value: A): F[A]

  def flatMap[A, B](value: F[A])(func: A => F[B]): F[B]
}
```

`pure` is a Monad Constructor. Every monad is expected to provide the ability to create new instances.
The `F[_]` syntax implies that this `Type Class` is applicable to Generic Types with a 
single Type argument like `List[T]`, and  `Set[T]`.
We could make our `Container` a instance of the Cats `Monad` `Type Class`

```
class ContainerV2[+A](val item:A)

val monadInstanceForContainer = new Monad[ContainerV2] {

  override def flatMap[A, B](fa: ContainerV2[A])(f: A => ContainerV2[B]): ContainerV2[B] = f(fa.item)

  override def tailRecM[A, B](a: A)(f: A => ContainerV2[Either[A, B]]): ContainerV2[B] = ???

  override def pure[A](x: A): ContainerV2[A] = new ContainerV2(x)
}
```
As usual, Cats provides Monad instances for many of Scala Standard Library Classes.
Some of these instances may be redundant because classes like Option , List, etc already have `flatMap` defined.
To become part of the Cats Monad Type Class, we will also have to implement `tailRecM`.
I will try to cover `tailRec` in another post.

### Monad Flavours In Cats
Every Monad has a `flatMap` method. 
In the case of `Option` and our `Container` we see how `flatMap` has been implemented to support Error Handling.
It turns out that flatMap can be repurposed to achieve various other goals.
We will see later in this post how `flatMap` can be given a completely different flavour 
totally unrelated to Error Handling.

Let us take a look at a few of the Monad flavours.
### The Id Monad

[github link](https://github.com/dalgado-aws/ScalaCatsIntro/blob/main/src/main/scala/toppackage/h_MonadFlavours_6_Id.scala)

We saw that the `Option` monad provides graceful error handling while chaining function.
>What functionality does the `Id` monad provide to help with function chaining.

The answer is nothing! The `Id` monad does not really do anything.
It allows us to treat ordinary literals like "1", 2, "hello" , 33.3 as Monads.

It does not seem very useful at first glance. 
We will find its utility when we wade deeper into functional programming.
In certain situations, we have have functions that take a Monad as parameter.
The Id Monad will allow us to invoke those functions on ordinary types like Int, String, etc
but converting these types to a Monad.


For now, lets see how to create and use the cats.Id monad.
```
  val i:cats.Id[Int] = 22

  val j = 33:cats.Id[Int]

  val k:cats.Id[Int] = cats.Monad[Id].flatMap(i){x:Int => 33} 
```

Note that the `flatMap` signature seems to be very similar to `map`.
The function taken in by `flatMap` should have returned `Id[Int]`. It is returning `Int` instead.

It works because the way `Id` is defined. `type Id[A] = A`

#### Either - Get More Info About Error In A Chain

[github](https://github.com/dalgado-aws/ScalaCatsIntro/blob/main/src/main/scala/toppackage/g_MonadFlavours_1_Either.scala)

`Either` is very similar to `Option`. `Option` allows us to chain function and handle intermediate errors.
`Either` provides more information about the error.

`Either` is provided in the Scala Standard Library. 
The Cats library provides additional helper methods.
```
  val f1 = (x:Int) => Right(x + 1)

  val f2 = (x:Int) => Right(x + 2)

  val f3_cannot_process_input = (x:Int) => Left("Error")

  val f3 = (x:Int) => Right(x + 3)

  val chain = Right(1).flatMap(f1).flatMap(f2).flatMap(f3_cannot_process_input).flatMap(f3)

  val defaultOnError = -1

  val chainResult = chain.getOrElse(defaultOnError)
```
Cats provides utility and helper methods
```
33.asRight[String]
```

### Eval - Eager, And Lazy Evaluation Of Chain Components

[github link](https://github.com/dalgado-aws/ScalaCatsIntro/blob/main/src/main/scala/toppackage/g_MonadFlavours_2_Eval.scala)

`Eval` again allows us to chain functions.  
We need to emphasize that `Eval` has same signature as `Option`
and `Either` i.e. `Eval[Int]` it has a `flatMap` method that takes `Int` and returns `Eval[Int]`.
However, unlike `Option` and `Either`, `Eval` has nothing to do with error handling.

What `Eval` provides us is the ability to chain functions that have varying evaluation characteristics.
Let us see an example to see what this means.
```

  val now = Eval.now {

    print("m1. Evaluating 'now' at definiton time. Once and for all!")

    val a = 100

    val b = 100

    a + b
  }

  val later = Eval.later {

    print("m2. Evaluating 'later'. When first called!")

    val c = 100

    val d = 100

    c + d
  }

  val always = Eval.always {

    print("m3. Evaluating 'always', again, and again, and again ...")

    val e = 100

    val f = 100

    e + f
  }

  val result = now.flatMap(i=>later.flatMap(j=> always.map(k=> i+j+k)))

  println("*************************************************************************")

  println("first call", result.value)

  println("*************************************************************************")

  println("second call", result.value)

  println("*************************************************************************")

  println("third call", result.value)
```
"m1" will be printed just once when `val now = ...` is defined.

"m2" will be printed just once when `result.value` is invoked in the "first call"

"m3" will be printed thrice, at "first call", "second call", and "third call".

Eval.now is like `val`. Eval.later is like `lazy val`. Eval.always is like `def`

### Writer - Log Info For Every Function In The Chain 

[github link](https://github.com/dalgado-aws/ScalaCatsIntro/blob/main/src/main/scala/toppackage/g_MonadFlavours_3_Writer.scala)

Writer Monad passes along a "log" along with the result value.
In a multi threaded applications, logs of various threads get mixed up.
One solution is to have a thread id with every log message.
Another solution is to carry along the log with the data that is being computed and get the final result and all the 
log associated with the data in one place.

Let us see how that would work.
```
 import cats.data.Writer

  val applyHolidayDiscount = (price:Double) => Writer(List(s"applying holiday discount 2% off ${price} => ${price*0.98}"), price*0.98)

  val applyingEmployeeDiscount = (price:Double) => Writer(List(s"applying employee discount 3% off ${price} => ${price * 0.97}"), price * 0.97 )

  val applyingMembershipDiscount = (price:Double) => Writer(List(s"applying membership discount 2% off ${price} => ${price * 0.98}"), price * 0.98 )

  val startPrice = Writer(List("Start price is 1000"), 1000d)

  val discountedPrice = Writer(List("Processing start price of 1000"), 1000.0).
    flatMap(applyHolidayDiscount).
    flatMap(applyingEmployeeDiscount).
    flatMap(applyingMembershipDiscount)

  //cap off discount to 90% of start price

  val finalPrice = discountedPrice.flatMap(
    dp => startPrice.flatMap(

      sp => {

        if(dp > 0.9 * sp)

          Writer(List("Capping discount to 90%"), sp*0.9)

        else

          Writer(List("Discount price approved!"), dp)
      }
    )
  )
  finalPrice.value // the final value

  finalPrice.written // the log

```

### Monad Cost
Every composition using `flatMap` results in the creation of another `Monad` instance!
This cost has to be kept in mind while chaining functions with monads.

### Reader Monad 

[github link](https://github.com/dalgado-aws/ScalaCatsIntro/blob/main/src/main/scala/toppackage/g_MonadFlavours_4_Reader.scala)

The Monads that we have seen till now are quite similar.
They carry along the result(or error) along a chain and maybe some extra information as well.
For e.g. `Option` carries along the result or an error indication.
`Either` carries along the result or error and more info about the error.
`Writer` carries along Log information.
This may lead us to believe that that it all there is to a Monad pattern.
The `Reader` and `State` Monads will show that there are other ways `flatMap` can be implemented.

Like other monads, the Reader Monad has `flatMap` and can be chained, but it has nothing to do with carrying around error information along the chain.
Instead, it carries around a `Reader`.   

Let us see how that works with an example.
Suppose we have two functions that have `income` as an input parameter:
```
  val income = 99999
  // funtion 1 has a input dependecy on income
  def stateTax(income:Int):Double = income * 0.1

  // function 2 also has a input dependency on income
  def federalTax(income:Int):Double =  income * 0.01

```
How can we combine these two functions to produce another function that takes `income` as an input parameter?
The straight forward way would be to create a third function:
```
  // 1. Combining two function having same dependency without Reader
  def combineBothFunctionsWithoutReader(income:Int) = {

    val stateTax = stateTax(income)

    val federalTax = federalTax(income)

     stateTax + federalTax
  }
  print("Combine Without Reader", combineBothFunctionsWithoutReader(INCOME))
```
Reader Monad allows us to combine these two functions to create another function that takes the same input parameter
```
  // 2. Combining two function having same dependency using Reader
  val incomeReaderForStateTax = Reader(stateTax)

  val incomeReaderForFederalTax = Reader(federalTax)

  val  combineBothFunctionsWithReader = incomeReaderForStateTax.flatMap(stateTax =>

    incomeReaderForFederalTax.flatMap(federalTax =>

      Reader((costPrice:Int)=> salesTax + federalTax))))

  print("Combine With Reader", combineBothFunctionsWithReader.run(INCOME))
```
We are combining/chaining two functions that both depend on `income`, to yield another function that also depends on
`income`
Readers can also be used to combine functions that do not have the same input parameter. 
See my comment here[linke to stack overslow]()

### State

[github link](https://github.com/dalgado-aws/ScalaCatsIntro/blob/main/src/main/scala/toppackage/g_MonadFlavours_5_State_1.scala)

[github link](https://github.com/dalgado-aws/ScalaCatsIntro/blob/main/src/main/scala/toppackage/g_MonadFlavours_6_State_2.scala)

Object Oriented Programming has syntactic constructs to gather data and the functions that act on that data in one place.
That is what `classes` are.
In Functional Programming, functions and data are kept separate.
We prefer functions to be Pure, with no state and side effects.

In certain situations, however, we need to parcel the data with the functions that act on the data.

We want to pass on the data from function to function. State Monad allows us to do that.
 ```
import cats.data.State

  val firstFunction = (s:Int) => (s+1, 1)
  val secondFunction = (s:Int) => (s+2, 1)
  val thirdFunction = (s:Int) => (s+3, 1)

  val a = State(firstFunction)
  val b = State(secondFunction)
  val c = State(thirdFunction)

  a.flatMap(as => b.flatMap(bs => c.map( cs => s"final State ${cs}")))
```

### Special Syntax For Monads In Scala
This post emphasises the "chaining" aspect of Monads. We have tried to make the chains explicit.

Scala provides another syntax that makes the chain more readable.
This is the `for comprehension` syntax.
```
  val optionOne = Option(1)
  val optionTwo = Option(2)
  val result1 = optionOne.flatMap(o1Value => optionTwo.map(o2Value => o1Value + o2Value))
  
  val result2 = for {
    o1Value <- optionOne
    o2Value <- optionTwo
  } yield o1Value + o2Value
```

### Monad Transformers

[github link](https://github.com/dalgado-aws/ScalaCatsIntro/blob/main/src/main/scala/toppackage/h_MonadTransformers.scala)

Once we start using Monads extensively, we sometimes end up with "nested" Monads.
For e.g., we may end up with `Option[Option[String]]`, or `List[Option[String]]`, or `Either[Option[String]]`

Although they look different, all 3 types mentioned above represent a `String` encapsulated by various "contexts"

Monad Transformers makes it easier to work with these types of nested monads.
Let us see how this works.
```
import cats.data.OptionT
import cats.implicits._

  val resultOne:Either[String, Option[Int]] = Right(Option(1))
  val resultTwo:Either[String, Option[Int]] = Right(Option(2))

  val result =
    for {
    r1 <- OptionT(resultOne)

    r2 <- OptionT(resultTwo)

  } yield r1 + r2

  println(result.value)

```

### Conclusion
To become effective functional programmers we need to understand why Monads are useful and how they work.
This post tries to  explore some of Monads made available to us in the Cats library.
  
### References
- [Herding Cats](https://eed3si9n.com/herding-cats/sbt.html)
- [Identity Monad by Douglas Crockford - Paid Site](https://frontendmasters.com/courses/javascript-the-good-parts/the-identity-monad/)
- [Reader Monad Implementation ]( https://stackoverflow.com/questions/29174500/reader-monad-for-dependency-injection-multiple-dependencies-nested-calls/65390350#65390350 )
- [Monad Transformers](https://www.youtube.com/watch?v=TX-DKxF_K8U)
