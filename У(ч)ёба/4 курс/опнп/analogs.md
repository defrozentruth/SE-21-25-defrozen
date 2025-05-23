
# Сравнение аналогов

## Принцип отбора аналогов

В роли сравнительных аналогов были рассмотрены технологии для реализации параллельных вычислений на графическом процессоре. Основным критерием служила возможность работы с массивами, состоящими из чисел с плавающей точкой. Подбор аналогов осуществлялся с использованием ресурса Google Scholar. Для поиска применялся следующий запрос: "параллельное программирование GPU". По данному запросу был получен следующий список аналогов: OpenCL, CUDA, ROCm, Vulkan, DirectCompute. Несмотря на то, что представленные в списке аналогов технологии находятся на разных уровнях абстракции (OpenCL — стандарт, CUDA и ROCm — платформы, Vulkan и DirectCompute — API), все они предоставляют доступ к необходимому для задач радиомониторинга низкоуровоневому API, позволяющему выполнять задачи общего назначенния на графических процессорах (GPGPU), в том числе вычисления над массивами, содержащими числа с плавающей точкой.

### OpenCL
OpenCL (Open Computing Language) — это открытый стандарт, предназначенный для создания программ, которые могут выполняться на центральных и графических процессорах. OpenCL позволяет проводить вычисления на графических и центральных процессорах с помощью API, реализованного на адаптированной версии C — OpenCL C. OpenCL обеспечивает платформонезависимость и позволяет использовать одно и то же приложение на оборудовании разных производителей, таких как AMD, Intel и NVIDIA [1, 2, 3, 4].

### CUDA
CUDA (Compute Unified Device Architecture) — это проприетарная платформа и набор инструментов, разработанный компанией NVIDIA для вычислений на их графических процессорах. CUDA предоставляет упрощенные API и инструменты для ускорения разработки параллельных приложений. Основным ограничением является привязанность к оборудованию NVIDIA [4, 5].

### ROCm
AMD ROCm (Radeon Open Compute) — это программная платформа с открытым исходным кодом, предназначенная для вычислений на графических процессорах и ориентированная в первую очередь на высокопроизводительные вычисления (HPC), машинное обучение и другие приложения с интенсивными вычислениями. Он предоставляет разработчикам основу для написания портативных и высокопроизводительных приложений для графических процессоров AMD[6].

### Vulkan
Vulkan — это высокопроизводительный низкоуровневый API, предназначенный в первую очередь для графических и вычислительных задач. Он обеспечивает явный контроль над ресурсами и операциями графического процессора, обеспечивая расширенную оптимизацию. Вычислительные возможности Vulkan позволяют разработчикам выполнять вычисления на графическом процессоре общего назначения (GPGPU). API очень гибок и поддерживает ряд платформ, таких как Windows, Linux, macOS, Android, а также различных поставщиков графических процессоров, включая NVIDIA, AMD и Intel [7]. 

### DirectCompute
DirectCompute является частью API Microsoft DirectX и специально разработан для выполнения вычислительных операций на графических процессорах. Он интегрирован с другими компонентами DirectX, что делает его особенно полезным для приложений, предназначенных для Windows. Хотя DirectCompute обеспечивает мощные вычисления с ускорением на графическом процессоре, его основное внимание уделяется платформам на базе Windows[8, 9].

## Критерии сравнения аналогов

### Совместимость с оборудованием
Данный критерий оценивает количество устройств, поддерживающих работу с технологией. Чем их больше, тем выше оценка.

### Производительность
В данном критерии оценивается скорость выполнения технологией вычислений. Тестирование производилось на одинаковом оборудовании в виде перемножения ста пар матриц чисел с плавающей точкой размера 2000x2000[10]. Чем меньше время выполнения, тем выше оценка.

### Обучаемость
Данный критерий отражает уровень сложности в освоении технологии. Этот критерий включает в себя доступность обучающих материалов, примеров кода и общую сложность освоения.

## Таблица сравнения аналогов

|Аналог|Совместимость с оборудованием         |Производительность|Обучаемость 
|------|--------------------------------------|------------------|-----------
|OpenCL| Устройства от Nvidia, AMD, Intel, ARM|0.2-1 секунд     |API,требующее знание платформ и драйверов; ограниченное количество документации и учебных материалов; множество примеров кода, но они часто требуют адаптации для разных платформ
| CUDA | Только видеокарты Nvidia             |0.1-0.5 секунд     |API, подходящее для новичков; большое количество документации и курсов от самой Nvidia; множество примеров кода, не требующей адаптации под конкретное устройство. 
| ROCm |     Устройства от Nvidia, AMD        |0.1-0.5 секунд     |API, подходящее для новичков, особенно для разработчиков, знакомых с CUDA; малое количество примеров кода и обучающих материалов. 
| Vulkan | Устройства от Nvidia, AMD, Intel, ARM             |0.3-0.5 секунд     |Сложное API; малое количество примеров кода и обучающих материалов 
| DirectCompute | Только Windows в связке с видеокартами, поддерживающими DirectX(Nvidia, AMD)            |0.5-1 секунд     |API с меньшим порогом вхождения для разработчиков, знакомых с DirectX; малое количество обучающих материалов и примеров кода.             


## Выводы по итогам сравнения

В результате сравнения технологий можно сказать, что универсального решения не существует, все технологии имеют преимущества и недостатки. 

- OpenCL сложен в освоении, но дает возможность реализовывать код на CPU и GPU от различных производителей, однако, реализация на устройстве конкретного производителя может потребовать специфической оптимизации. Имеет большой разброс по скорости выполнения в виду необходимости дополнительной оптимизации под конкретное устройство.
- CUDA более проста в освоении, но не имеет вариативности в выборе платформы, однако это дает и преимущество в виде отсутствия необходимости дополнительной адаптации и оптимизации кода под конкретное устройство. Имеет один из самых высоких показателей по скорости выполнения.
- ROCm более простой в освоении, но ограничен платформами от Nvidia и AMD. Имеет один из самых высоких показателей по скорости выполнения.
- Vulkan сложен в освоении, но дает возможность реализовывать код на CPU и GPU от различных производителей, однако, реализация на устройстве конкретного производителя может потребовать специфической оптимизации. Также технология позволяет работать с устройством на низком уровне, что поможет при процессе оптимизации. Имеет средний показатель по скорости выполнения.
- DirectCompute более простой в освоении, но при условии, что разработчик уже знаком с DirectX. Технология также накладывает сильные ограничения из-за своей привязки к операционной системе Windows. Имеет средние показатели по скорости выполнения.

## Выбор метода решения
Для текущей задачи проведения параллельных вычислений над массивами, содержащими числа с плавающей точкой, была выбрана технология CUDA. Она обладает более низким порогом вхождения и превосходит аналоги по скорости вычислений на видеокартах Nvidia, что ускорит выполнение программы, а так же избавит от необходимости реализации специфической оптимизации, так как она будет выполнятся на системе с видеокартой от Nvidia. Решение должно представлять программный код, разработанный при помощи CUDA.

## Список использованных источников
1. Gaster, B., Howes, L., Kaeli, D., Mistry, P., & Schaa, D. (2011). Heterogeneous Computing with OpenCL: Revised OpenCL 1.2 Edition. Elsevier.
2. Stone, J. E., Gohara, D., & Shi, G. (2010). OpenCL: A parallel programming standard for heterogeneous computing systems. Computing in Science & Engineering
3. Tsuchiyama, R., Nakamura, T., Iizuka, T., and Asahara, A., The OpenCL Programming Book, Fixstars Corporation, 2010.
4. [CUDA Toolkit Documentation](https://docs.nvidia.com/cuda/) 
5. Fang, J., Varbanescu, A. L., & Sips, H. (2011). A comprehensive performance comparison of CUDA and OpenCL. Proceedings of the 2011 International Conference on Parallel Processing (ICPP), 216–225. DOI: 10.1109/ICPP.2011.45. 
6. [ROCm](https://www.amd.com/en/products/software/rocm.html)
7. [Vulkan](https://community.khronos.org/c/vulkan/24)
8. Розенбаум Александр Евгеньевич, Глазков Андрей Валерьевич Современные возможности организации высокопроизводительных вычислений с использованием персональных ЭВМ // Вестник ЮУрГУ. Серия: Компьютерные технологии, управление, радиоэлектроника. 2012. №3 (262). URL: https://cyberleninka.ru/article/n/sovremennye-vozmozhnosti-organizatsii-vysokoproizvoditelnyh-vychisleniy-s-ispolzovaniem personalnyh-evm (дата обращения: 04.12.2024).
9. [DirectCompute](https://learn.microsoft.com/ru-ru/windows/win32/direct3d11/direct3d-11-advanced-stages-compute-shader) 
10.Bassam Shaer, Timothy Stewart 2023 Optimize Matrix Multiplication Utilizing OpenCL FPGA Kernel
