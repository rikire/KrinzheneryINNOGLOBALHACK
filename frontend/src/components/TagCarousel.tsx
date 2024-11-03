import React, { useEffect, useRef } from 'react';
import { Tag } from './Tag';

type TagCarouselProps = {
  tags: string[];
};

export const TagCarousel: React.FC<TagCarouselProps> = ({ tags }) => {
  const carouselRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    const carousel = carouselRef.current;
    if (!container || !carousel) return;
    // Функция для обновления состояний скролла
    const updateScrollStatus = () => {
      if (carousel.scrollLeft > 5) {
        container.classList.add('TagCarousel_hasRight');
      } else {
        container.classList.remove('TagCarousel_hasRight');
      }

      if (
        carousel.scrollLeft <
        carousel.scrollWidth - carousel.clientWidth - 5
      ) {
        container.classList.add('TagCarousel_hasLeft');
      } else {
        container.classList.remove('TagCarousel_hasLeft');
      }
    };

    updateScrollStatus(); // Обновить состояния при монтировании
    carousel.addEventListener('scroll', updateScrollStatus); // Обновить при прокрутке

    // Очистка слушателя события при размонтировании
    return () => container.removeEventListener('scroll', updateScrollStatus);
  }, []);

  // Функция для прокрутки влево
  const scrollLeft = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (carouselRef.current) {
      carouselRef.current.scrollBy({
        left: -200,
        behavior: 'smooth',
      });
    }
  };

  // Функция для прокрутки вправо
  const scrollRight = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (carouselRef.current) {
      carouselRef.current.scrollBy({
        left: 200,
        behavior: 'smooth',
      });
    }
  };

  return (
    <div className="TagCarousel-Container" ref={containerRef}>
      <button
        className="TagCarousel-ButtonRight"
        onClick={scrollLeft}
        aria-label="Предыдущие репозитории">
        {' '}
        <div className="TagCarousel-ButtonShadow" />
      </button>

      <div ref={carouselRef} className="TagCarousel">
        {tags.map((tag, index) => (
          <Tag key={index} view="default">
            {tag}
          </Tag>
        ))}
      </div>
      <button
        className="TagCarousel-ButtonLeft"
        onClick={scrollRight}
        aria-label="Следующие репозитории">
        <div className="TagCarousel-ButtonShadow" />
      </button>
    </div>
  );
};
